# -*- coding: iso-8859-15 -*-

""" moinmoin-Plugin fuer den Export oder die Anzeige von Lastschrift-Vorlagen

Die folgenden Aufrufe sind moeglich:

  # inline-Anzeige einer Lastschrift-Vorlage fuer die Mitglieder-Daten auf der aktuellen Wiki-Seite
  <<OpennetLastschrift()>>

  # Anzeige aller Lastschrift-Vorlagen fuer einen Monat (hier: April)
  <<OpennetLastschrit(4)>>

  # Download-Link fuer die Lastschrift-Vorlagen eines Monats (hier Juli)
  <<OpennetLastschrit(7, link_only=True)>>
"""
import csv
import datetime
import re
import StringIO

from MoinMoin import wikiutil
from MoinMoin.action import cache


WIKIPAGE_MITGLIEDERLISTE = u"Mitglieder"
ZIEL_IBAN = u"DE59830654080004809602"
ZIEL_NAME = u"Opennet Initiative e.V."
DEFAULT_VERWENDUNGSZWECK1 = u"Investitionskostenzuschuss"
# das fuehrende Leerzeichen dient zur Abgrenzen von der vorherigen Zeile - das passiert wohl sonst nicht
VERWENDUNGSZWECK2 = u" Opennet Initiative e.V."
STANDARD_BETRAG = 1.00
GLAEUBIGER_ID = u"DE15ZZZ00000889771"
BEITRAGS_FORMAT = re.compile(r"^(?P<period>[QJ])(?P<month>[0-9]+)=(?P<value>[0-9.]+)$")
MONATSNAMEN = ("Januar", "Februar", "Maerz", "April", "Mai", "Juni", "Juli", "August", "September",
               "Oktober", "November", "Dezember")
# die Skatbank erwartet iso8859-15
OUTPUT_ENCODING = "iso8859-15"
# die Skatbank akzeptiert nur die folgenden Buchstaben als Ziel einer Überweisung
TRANSFER_TARGET_NAME_REGEX = re.compile(u"[^ a-zA-Z0-9äöüßÄÖÜ.,&\-/+*>$%]")


class BeitragsFormatError(Exception):
    pass


class Mitglied(object):

    def __init__(self, request, page_name):
        self.request = request
        self.page_name = page_name

    def get_dict_value(self, key, default=None):
        key = wikiutil.get_unicode(self.request, unicode(key), 'key')
        data_dict = self.request.dicts.get(self.page_name, {})
        try:
            result = data_dict[key]
        except KeyError:
            result = "" if default is None else default
        return result.encode("utf8")

    def get_name(self):
        vorname = self.get_dict_value("Vorname")
        nachname = self.get_dict_value("Nachname")
        if vorname:
            return "{} {}".format(vorname, nachname)
        else:
            return nachname

    def _parse_beitrag(self):
        result = {}
        for token in self.get_dict_value("Beitragsmodell").split():
            match = BEITRAGS_FORMAT.match(token)
            if match:
                data = match.groupdict()
                month = int(data["month"])
                value = float(data["value"])
                period = data["period"]
                if (((period == "Q") and (month in (1, 2, 3)))
                        or ((period == "J") and (month in range(1, 13)))):
                    if period not in result:
                        result[period] = {}
                    result[period][month] =  value
                    continue
            # irgendeine der obigen Pruefungen schlug fehl
            raise BeitragsFormatError("Fehlerhaftes Beitragsformat fuer {}: {}"
                                      .format(self.get_name(), token))
        return result

    def get_beitrag_jahr(self, month):
        if not self.is_paying_member():
            return None
        parsed = self._parse_beitrag()
        try:
            return parsed["J"][month]
        except KeyError:
            return None

    def get_beitrag_quartal(self, month):
        if not self.is_paying_member():
            return None
        parsed = self._parse_beitrag()
        # die Quartalsmonate werden von 1..3 gezaehlt
        month_in_quartal = (month - 1) % 3 + 1
        try:
            return parsed["Q"][month_in_quartal]
        except KeyError:
            return None

    def _parse_boolean_value(self, key):
        raw = self.get_dict_value(key)
        if raw == "ja":
            return True
        elif raw == "nein":
            return False
        else:
            raise BeitragsFormatError("Unerlaubter Inhalt im Feld '{}' fuer {}: {} (ja/nein)"
                                      .format(key, self.get_name(), raw))

    def is_paying_member(self):
        return self._parse_boolean_value("Mitgliedschaft") \
            and not self._parse_boolean_value("Zahlungsaussetzung")

    def _get_safe_transfer_target_name(self):
        name = self.get_dict_value("Kontoinhaber") or self.get_name()
        name = unicode(name, "utf-8")
        return TRANSFER_TARGET_NAME_REGEX.sub(u"", name).encode("utf-8")

    def _get_shorted_name(self, text, max_count):
        if (len(text) > max_count) and text.endswith(" e.V."):
            text = text[:-5]
        if len(text) > max_count:
            return "{}..{}".format(text[:max_count // 2 - 1], text[-(max_count // 2 - 1):])
        else:
            return text

    def get_lastschrift_fields(self, betrag, verwendungszweck):
        """
        lastschrift_name, kontoinhaber, adresse, laender-kennzeichen, land, iban_quelle, bic_quelle, bank, betrag, verwendungszweck1,
        verwendungszweck2, iban_ziel, empfaenger, mandat, mandat_datum, glaeubiger_id
        """
        # Umwandlung von "2017-12-31" in "31.12.2017"
        datum_convert = lambda dash_str: ".".join(reversed(dash_str.split("-")))
        # das erste Feld ("Titel der Überweisung") darf nur 20 Zeichen lang sein
        fields = (self._get_shorted_name(self._get_safe_transfer_target_name(), 20),
                  self.get_name(),
                  "",
                  "",
                  "",
                  self.get_dict_value("IBAN"),
                  self.get_dict_value("BIC"),
                  self.get_dict_value("Bank"),
                  "{:0.2f}".format(betrag).replace(".", ","),
                  verwendungszweck,
                  VERWENDUNGSZWECK2,
                  ZIEL_IBAN,
                  ZIEL_NAME,
                  self.get_dict_value("MandatsID"),
                  datum_convert(self.get_dict_value("Mandatsdatum")),
                  GLAEUBIGER_ID)
        return fields

    @classmethod
    def get_lastschrift_header_fields(self):
        """ die Skatbank erwartet wohl genau diesen Header bei einer hochzuladenden CSV-Datei """
        header = (u"Bezeichnung der Basislastschrift",
                  u"Zahlungspflichtiger",
                  u"Adresse",
                  u"Länder-Kennzeichen",
                  u"Land",
                  u"IBAN des Zahlungspflichtigen",
                  u"BIC",
                  u"Bei Kreditinstitut",
                  u"Betrag",
                  u"Verwendungszweck 1",
                  u"Verwendungszweck 2",
                  u"IBAN des Zahlungsempfängers",
                  u"Zahlungsempfänger",
                  u"Mandatsreferenz",
                  u"Unterschrieben am",
                  u"Gläubiger ID des Zahlungsempfängers")
        return [text.encode("utf-8") for text in header]


def get_all_mitglieder(request):
    pages_regex = re.compile("^{}/".format(re.escape(WIKIPAGE_MITGLIEDERLISTE)))
    pages = request.rootpage.getPageList(filter=pages_regex.match)
    for page_name in sorted(pages):
        yield Mitglied(request, page_name)


def get_lastschrift_csv(request, page_name, month=None):
    csv.register_dialect("bank", delimiter=";", doublequote=False, quoting=csv.QUOTE_ALL)
    result_buffer = StringIO.StringIO()
    writer = csv.writer(result_buffer, dialect="bank")
    entries = []
    beitragssumme = 0
    if month is None:
        # Lastschriftvorlage fuer ein einzelnes Mitglied
        mitglied = Mitglied(request, page_name)
        entries.append(mitglied.get_lastschrift_fields(STANDARD_BETRAG, DEFAULT_VERWENDUNGSZWECK1))
        beitragssumme += STANDARD_BETRAG
    elif month not in range(1, 13):
        raise BeitragsFormatError("FEHLER: invalid month ({})".format(month))
    else:
        entries.append(Mitglied.get_lastschrift_header_fields())
        for mitglied in get_all_mitglieder(request):
            quartals_beitrag = mitglied.get_beitrag_quartal(month)
            jahres_beitrag = mitglied.get_beitrag_jahr(month)
            if quartals_beitrag:
                entries.append(mitglied.get_lastschrift_fields(quartals_beitrag,
                                                               "Quartalsbeitrag"))
                beitragssumme += quartals_beitrag
            if jahres_beitrag:
                entries.append(mitglied.get_lastschrift_fields(jahres_beitrag, "Jahresbeitrag"))
                beitragssumme += jahres_beitrag
    for dataset in entries:
	writer.writerow(dataset)
    content = result_buffer.getvalue().decode("utf8")
    return content, len(entries), beitragssumme


def _get_max_integer_field(request, key):
    """ find the highest integer value of a specific member dictionary field """
    number_regex = re.compile(r"^[0-9]+$")
    max_value = 0
    for member in get_all_mitglieder(request):
        value_string = member.get_dict_value(key)
        if value_string and number_regex.match(value_string):
            max_value = max(max_value, int(value_string))
    return max_value


def macro_OpennetLastschrift(macro, month=None, link_only=False):
    request = macro.request
    formatter = macro.formatter
    page = macro.formatter.page

    if month is not None:
        month = int(month)
    try:
        csv_content, entry_count, summe = get_lastschrift_csv(request, page.page_name, month)
    except BeitragsFormatError as exc:
        return u"""<pre>ERROR: {}</pre>""".format(str(exc).decode("utf8"))
    if link_only:
        cache_key = cache.key(request, content=csv_content)
        if not cache.exists(request, cache_key):
            filename_datestamp = datetime.datetime.now().strftime("%Y%m%d")
            cache.put(request, cache_key, csv_content.encode(OUTPUT_ENCODING, errors="ignore"),
                      content_type="text/csv",
                      content_disposition="attachment",
                      filename="opennet_lastschriften_{}.csv".format(filename_datestamp))
        return (u"""<a href="{}">Lastschriften-Export {} ({:d}): {:d} Euro</a>"""
                .format(cache.url(request, cache_key),
                        MONATSNAMEN[month - 1] if month else "einzeln", entry_count - 1, int(summe)))
    else:
        return u"""<pre>{}</pre>""".format(csv_content)


def macro_OpennetNextUnusedFieldValue(macro, key):
    request = macro.request
    return u"{:d}".format(_get_max_integer_field(macro.request, key) + 1)
