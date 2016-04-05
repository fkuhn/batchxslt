<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema" xmlns:cmd="http://www.clarin.eu/cmd/"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" exclude-result-prefixes="xd" version="2.0">

    <!-- DGDEVENT2CMDI
    
    CHANGELOG:
    v3.5 (May 2nd 2015)
    - Disabled Geolocations - latitude and longitude elements. Note that grid element is kept.
    - removed href attribute for non-Relation.SubElements
    
    
    v3.4.1 (Mar 08th 2015)
    - Removed: ./Basisdaten/Relation_zu_SE-Aufnahme/Vollständigkeit/text() to "Integrity". Not a useful Element.
    - FIXED: FOLK - each "Transkript/Erstellung/Instrumente/text()" not being tokenized to multiple TranscriptionTool Elements.
    
    v3.4 (Mar 07th 2015):
    - Element FileUri removed. Added href attribute to FileName element for reference to file when browsing data.
    - NOTE: value of href is determined with batchxslt or JLZa after xslt processing.
    - FIXED: now n instances of "Instrumente" in //Transkript/Annotation/Erstellung are transformed.
    - FIXED: now n instances of tokenized participating technicians and scientists are generated. 
    - FIXED: Filenames of n transcripts are now single instances. 
    - TODO: remove unnecessary parameter definitions. direct element value access is sufficient.
    - TODO: replace "nicht dokumentiert" and "nicht vorhanden" with "not listed" and "none". also add xml:lang="eng"
    - TODO: replace zero values for population with "not filed" adding xml:lang="eng". 
    
    v3.3.2:
    - every select statement on text values now features normalize-space()
    
    v3.3.1:
    - FIXED: double nesting of FileName Element in Transcripts
    - added output method definitions (xml, indented).
    
    v3.3:
    - Added 1..n Transcripts, 1..n Sessions and 1..n Recording
    - if clause for testing type of mediafile reference (audio or video)
    
    v3.2:
    - FIXED: Transcript references for looping ('.' operator).
    - Added FileLabel, FileName and FileURI for audio/video data. Note: Each event can either refer to an audio
    file or an audio file at the moment. the dgd schema does not allow both media types at the same time.
    FileURI is used by either via batchxslt or JLza to define the path to the actual data.
    - Added FileName for each Transcript.
    
    v3.1:
    - Added Transcript Element and its Subelements. Event- Transcript is a 1..n relation.
    
    v3:
    - Added "Inhalt" Elements (content-prefix) and its subelements as non nested cmdi-elements.
    - removed parameters for Speaker. 
    - added element TranscriptID ("Sigle_in_Transkripten").
    - FIXED: now generates more than one speaker if necessary.
    - FIXED: $environment now used.
    - FIXED: speaker languages addressed correctly.
    -->

    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 25, 2014</xd:p>
            <xd:p><xd:b>Author:</xd:b> Florian Kuhn</xd:p>

            <xd:p/>
        </xd:desc>
    </xd:doc>

    <!-- TODO: ENABLE SCHEMA AWARENESS Note: EE of Saxon required -->

    <!-- NAMESPACE DEFINITIONS -->
    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- DEFINE OUTPUT METHOD -->
    <xsl:output method="xml" indent="yes"/>

    <!-- PARAMETERS -->

    <!-- define parameters for CMDI header -->
    <xsl:param name="mdCreator" select="'DGD2CMDI'"/>
    <xsl:param name="mdCreationDate" select="current-date()"/>
    <xsl:param name="mdSelfLink" select="base-uri()"/>
    <xsl:param name="mdCollectionDisplayName" select="'AGD'"/>
    
    <!-- Profile ID that is assigned to each Resource profile in the 
    Clarin Compenent Registry (May 20th 2015)-->
    <xsl:param name="cmdProfile" select="'clarin.eu:cr1:p_1430905751615'"/>

    <!-- Resource Proxies parameters for CMDI header -->
    <xsl:param name="resourceProxyList" select="' '"/>
    <xsl:param name="journalFileProxyList" select="' '"/>
    <xsl:param name="resourceRelationList" select="''"/>

    <!-- define parameters for catalogue template -->
    <xsl:param name="title" select="/Ereignis/@Kennung"/>
    <xsl:param name="description" select="/Ereignis/Basisdaten[1]/Beschreibung[1]/text()"/>

    <xsl:param name="date" select="/Ereignis/Basisdaten[1]/Datum[1]/YYYY-MM-DD[1]/text()"/>
    <xsl:param name="institution" select="/Ereignis/Basisdaten[1]/Institution[1]//text()"/>
    <xsl:param name="environment" select="/Ereignis/Basisdaten[1]/Räumlichkeiten[1]/text()"/>
    <xsl:param name="duration" select="/Ereignis/Basisdaten[1]/Dauer[1]/text()"/>
    <xsl:param name="period" select="/Ereignis/Basisdaten[1]/Zeitraum[1]/text()"/>
    <xsl:param name="conditions" select="/Ereignis/Basisdaten[1]/Aufnahmebedingungen[1]/text()"/>
    <xsl:param name="type" select="/Ereignis/Sprechereignis[1]/Basisdaten[1]/Art[1]/text()"/>


    <!-- define parameters for staff template -->
    <xsl:param name="researcherParticipating"
        select="/Ereignis/Projekt/Personal/An_E_teilnehmende_Forscher/text()"/>
    <xsl:param name="technicianParticipating"
        select="/Ereignis/Projekt/Personal/An_E_teilnehmende_Techniker/text()"/>

    <!-- define parameters for location template -->
    <xsl:param name="country" select="/Ereignis/Basisdaten[1]/Ort[1]/Land[1]/text()"/>
    <xsl:param name="region" select="/Ereignis/Basisdaten[1]/Ort[1]/Region[1]/text()"/>
    <xsl:param name="district" select="/Ereignis/Basisdaten[1]/Ort[1]/Kreis[1]/text()"/>
    <xsl:param name="locationName" select="/Ereignis/Basisdaten[1]/Ort[1]/Ortsname[1]/text()"/>
    <xsl:param name="population" select="/Ereignis/Basisdaten[1]/Ort[1]/Einwohnerzahl[1]/text()"/>
    <xsl:param name="locationDistrict" select="/Ereignis/Basisdaten[1]/Ort[1]/Ortsteil[1]/text()"/>
    <xsl:param name="locationDescription"
        select="/Ereignis/Basisdaten[1]/Ort[1]/Ortsbeschreibung[1]/text()"/>
    <xsl:param name="grid"
        select="/Ereignis/Basisdaten[1]/Ort[1]/Koordinaten[1]/Planquadrat[1]/text()"/>
    
<!--    
        Latitude and Longitude are disabled for first ingest. 
        <xsl:param name="latitude"
        select="/Ereignis/Basisdaten[1]/Ort[1]/Koordinaten[1]/Geocode[1]/Geografische_Breite[1]/text()"/>
    <xsl:param name="longitude"
        select="/Ereignis/Basisdaten[1]/Ort[1]/Koordinaten[1]/Geocode[1]/Geografische_Länge[1]/text()"/>
-->
    <!-- Define speakers -->
    <xsl:param name="speakers">
        <xsl:value-of select="tokenize(/Ereignis/Sprechereignis/Sprecher/@Kennung,'\s;\s')"/>
    </xsl:param>

    <!-- define parameters for audio-metadata component -->
    <xsl:param name="format"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Tontechnische_Daten[1]/Format[1]/text()"/>
    <xsl:param name="codec"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Tontechnische_Daten[1]/Codec[1]/text()"/>
    <xsl:param name="samplingrate"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Tontechnische_Daten[1]/Abtastrate[1]/text()"/>
    <xsl:param name="quantization"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Tontechnische_Daten[1]/Quantisierungsrate[1]/text()"/>
    <xsl:param name="bitrate"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Tontechnische_Daten[1]/Datenrate[1]/text()"/>
    <xsl:param name="audioduration"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Basisdaten[1]/Dauer[1]/text()"/>

    <!-- define parameters for video metadata component -->
    <xsl:param name="videoformat"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Videotechnische_Daten[1]/Format[1]/text()"/>
    <xsl:param name="videocodec"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Videotechnische_Daten[1]/Codec[1]/text()"/>
    <xsl:param name="videoframerate"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Videotechnische_Daten[1]/Framerate[1]/text()"/>
    <xsl:param name="color"
        select="/Ereignis/Sprechereignis[1]/SE-Aufnahme[1]/Digitale_Fassung[1]/Videotechnische_Daten[1]/Farbe_Schwarz-weiß[1]/text()"/>

    <!-- TEMPLATES -->

    <!-- Define header template. document root -->
    <xsl:template match="/">
        <CMD xmlns="http://www.clarin.eu/cmd/" CMDVersion="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751615/xsd">
            <Header>
                <MdCreator>
                    <xsl:value-of select="$mdCreator"/>
                </MdCreator>
                <MdCreationDate>
                    <xsl:value-of select="$mdCreationDate"/>
                </MdCreationDate>
                <MdSelfLink>
                    <xsl:value-of select="$mdSelfLink"/>
                </MdSelfLink>
                <MdProfile>
                    <xsl:value-of select="$cmdProfile"/>
                </MdProfile>
                <MdCollectionDisplayName>
                    <xsl:value-of select="$mdCollectionDisplayName"/>
                </MdCollectionDisplayName>
            </Header>
            <Resources>
                <ResourceProxyList>
                    <xsl:value-of select="$resourceProxyList"/>
                </ResourceProxyList>
                <JournalFileProxyList>
                    <xsl:value-of select="$journalFileProxyList"/>
                </JournalFileProxyList>
                <ResourceRelationList>
                    <xsl:value-of select="$resourceRelationList"/>
                </ResourceRelationList>
            </Resources>
            <xsl:call-template name="cmd:Components"/>
        </CMD>
    </xsl:template>

    <!-- Define staff template -->
    <xsl:template name="cmd:Staff">
        <Staff>
            <xsl:for-each
                select="tokenize(/Ereignis/Projekt/Personal/An_E_teilnehmende_Forscher/text(), '\s;\s')">
                <ResearcherParticipating>
                    <xsl:value-of select="."/>
                </ResearcherParticipating>
            </xsl:for-each>
            <xsl:for-each
                select="tokenize(/Ereignis/Projekt/Personal/An_E_teilnehmender_Techniker/text(), '\s;\s')">
                <TechnicianParticipating>
                    <xsl:value-of select="."/>
                </TechnicianParticipating>
            </xsl:for-each>
        </Staff>
    </xsl:template>

    <!-- Define template Session 1..m -->

    <xsl:template name="cmd:Sessions">
        <xsl:for-each select="/Ereignis/Sprechereignis">
            <Session>
                <Label>
                    <xsl:value-of select="./@Kennung"/>
                </Label>
                <Title xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Titel/text()"/>
                </Title>
                <Content xml:lang="deu">
                    <xsl:value-of select="./Inhalt/Beschreibung/text()"/>
                </Content>

                <xsl:for-each select="tokenize(./Inhalt/Themen/text(), '\s;\s')">
                    <Subject xml:lang="deu">
                        <xsl:value-of select="."/>
                    </Subject>
                </xsl:for-each>

                <xsl:for-each select="tokenize(./Basisdaten[1]/Art[1]/text(), '\s;\s')">
                    <Type xml:lang="deu">
                        <xsl:value-of select="."/>
                    </Type>
                </xsl:for-each>

                <xsl:call-template name="cmd:Speakers"/>
                <xsl:call-template name="cmd:Recordings"/>
                <xsl:call-template name="cmd:Transcripts"/>
            </Session>
        </xsl:for-each>
    </xsl:template>

    <!-- Define location template -->
    <xsl:template name="cmd:Location">
        <Location>
            <Country xml:lang="deu">
                <xsl:value-of select="$country"/>
            </Country>
            <Region xml:lang="deu">
                <xsl:value-of select="$region"/>
            </Region>
            <District xml:lang="deu">
                <xsl:value-of select="$district"/>
            </District>
            <LocationName xml:lang="deu">
                <xsl:value-of select="$locationName"/>
            </LocationName>
            <Population>
                <xsl:value-of select="$population"/>
            </Population>
            <LocationDistrict xml:lang="deu">
                <xsl:value-of select="$locationDistrict"/>
            </LocationDistrict>
            <Coordinates>
                <Grid>
                    <xsl:value-of select="$grid"/>
                </Grid>
                <!--
                    Geocode Element is disabled since it is a future feature
                    <Geocode>
                    <Latitude>
                        <xsl:value-of select="$latitude"/>
                    </Latitude>
                    <Longitude>
                        <xsl:value-of select="$longitude"/>
                    </Longitude>
                </Geocode>-->
            </Coordinates>
        </Location>
    </xsl:template>

    <!-- Define Speaker Metadata Template in "Session"-Context -->

    <xsl:template name="cmd:Speakers">
        <!-- iterate over all Speaker elements and access their subvalues with the "." operator
        /Ereignis/Sprechereignis[1]/Sprecher[1]-->
        <xsl:for-each select="Sprecher">
            <Speaker>
                <Label>
                    <xsl:value-of select="./@Kennung"/>
                </Label>
                <TranscriptID>
                    <xsl:value-of select="./Basisdaten/Sigle_in_Transkripten/text()"/>
                </TranscriptID>
                <Sex xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Geschlecht/text()"/>
                </Sex>
                <Age>
                    <xsl:value-of select="./Basisdaten/Alter/text()"/>
                </Age>
                <Role xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Rolle/text()"/>
                </Role>
                <Language xml:lang="deu">
                    <xsl:value-of select="./Sprachdaten/Sprachen/text()"/>
                </Language>
            </Speaker>
        </xsl:for-each>
    </xsl:template>
    <!-- Template for Recordings. Define base data and test if recording is audio or video -->
    <xsl:template name="cmd:Recordings">
        <xsl:for-each select="SE-Aufnahme">
            <Recording>
                <Label>
                    <xsl:value-of select="./@Kennung"/>
                </Label>
                <xsl:for-each select="tokenize(./Basisdaten[1]/Typ[1]/text(), '\s;\s')">
                    <Type xml:lang="deu">
                        <xsl:value-of select="."/>
                    </Type>
                </xsl:for-each>
                <Duration>
                    <xsl:value-of select="./Basisdaten[1]/Dauer[1]/text()"/>
                </Duration>
                <xsl:if test="./Digitale_Fassung/Tontechnische_Daten">
                    <xsl:call-template name="cmd:SpeechTechnicalMetadata"/>
                </xsl:if>
                <xsl:if test="./Digitale_Fassung/Videotechnische_Daten">
                    <xsl:call-template name="cmd:VideoTechnicalMetadata"/>
                </xsl:if>
            </Recording>
        </xsl:for-each>
    </xsl:template>

    <!-- Technical Metadata: either an audio or a video file are defined per event. metadata schema does not allow audio and video files of one event -->

    <!-- Define Technical Audio Metadata Template. Warning: Note the context of this template is a <Recording>, "<SE-Aufnahme>". -->

    <xsl:template name="cmd:SpeechTechnicalMetadata">
        <AudioData>
            <FileLabel>
                <xsl:value-of select="./Digitale_Fassung[1]/@Kennung"/>
            </FileLabel>
            <FileName>
                <xsl:value-of select="./Digitale_Fassung[1]/Basisdaten/Dateiname/text()"/>
            </FileName>
            <Format>
                <xsl:value-of select="./Digitale_Fassung/Tontechnische_Daten/Format[1]/text()"/>
            </Format>
            <Codec>
                <xsl:value-of select="./Digitale_Fassung[1]/Tontechnische_Daten[1]/Codec[1]/text()"
                />
            </Codec>
            <SamplingRate>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Tontechnische_Daten[1]/Abtastrate[1]/text()"/>
            </SamplingRate>
            <Quantization>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Tontechnische_Daten[1]/Quantisierungsrate[1]/text()"
                />
            </Quantization>
            <BitRate>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Tontechnische_Daten[1]/Datenrate[1]/text()"/>
            </BitRate>
        </AudioData>
    </xsl:template>
    <!-- Define Video Metadata Template. "SE-Aufnahme"-Context -->
    <xsl:template name="cmd:VideoTechnicalMetadata">
        <VideoData>
            <FileLabel>
                <xsl:value-of select="./Digitale_Fassung[1]/@Kennung"/>
            </FileLabel>
            <FileName>
                <xsl:value-of select="./Digitale_Fassung[1]/Basisdaten/Dateiname/text()"/>
            </FileName>
            <Format>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Videotechnische_Daten[1]/Format[1]/text()"/>
            </Format>
            <Codec>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Videotechnische_Daten[1]/Codec[1]/text()"/>
            </Codec>
            <Framerate>
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Videotechnische_Daten[1]/Framerate[1]/text()"/>
            </Framerate>
            <Color xml:lang="deu">
                <xsl:value-of
                    select="./Digitale_Fassung[1]/Videotechnische_Daten[1]/Farbe_Schwarz-weiß[1]/text()"
                />
            </Color>
        </VideoData>
    </xsl:template>

    <!-- Define Transcript Metadata. Direct access to values due to for loop. -->
    <xsl:template name="cmd:Transcripts">
        <xsl:for-each select="Transkript">
            <Transcript>
                <Label>
                    <xsl:value-of select="normalize-space(./@Kennung)"/>
                </Label>
                <Title xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Titel/text()"/>
                </Title>
                <Type xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Typ/text()"/>
                </Type>
                <xsl:for-each select="./Digitale_Fassung/Basisdaten/Dateiname/text()">
                    <FileName>
                        <xsl:value-of select="."/>
                    </FileName>
                </xsl:for-each>
                <AnnotationConvention xml:lang="deu">
                    <xsl:value-of select="./Annotation/Basisdaten/Konventionen/text()"/>
                </AnnotationConvention>
                <RelatedEventLabel>
                    <xsl:value-of select="./Basisdaten/Relation_zu_SE-Aufnahme/@Kennung_SE-Aufnahme"
                    />
                </RelatedEventLabel>
                <!--<Integrity xml:lang="deu">><xsl:value-of
                        select="./Basisdaten/Relation_zu_SE-Aufnahme/Vollständigkeit/text()"
                    /></Integrity>
                -->
                <Period>
                    <xsl:value-of select="./Basisdaten/Relation_zu_SE-Aufnahme/Zeitabschnitt/text()"
                    />
                </Period>
                <Duration>
                    <xsl:value-of select="./Basisdaten/Relation_zu_SE-Aufnahme/Dauer/text()"/>
                </Duration>

                <!-- there are n Erstellung elements thus n Intrumente -->
                <xsl:for-each select="./Annotation/Erstellung">
                    <xsl:for-each select="tokenize(./Instrumente/text(), '\s;\s')">
                        <TranscriptionTool xml:lang="deu">
                            <xsl:value-of select="."/>
                        </TranscriptionTool>
                    </xsl:for-each>
                </xsl:for-each>
                <Alphabet xml:lang="deu">
                    <xsl:value-of select="./Basisdaten/Annotation/Basisdaten/Zeicheninventar/text()"
                    />
                </Alphabet>
                <Distribution xml:lang="deu">
                    <xsl:value-of select="./Distribution/@Stelle"/>
                </Distribution>
                <Access xml:lang="deu">
                    <xsl:value-of select="./Distribution/Zugänglichkeit/@Art"/>
                </Access>
            </Transcript>
        </xsl:for-each>
    </xsl:template>

    <!-- Define overall catalogue data structure -->
    <xsl:template name="cmd:Components">
        <Components>
            <DGDEvent>
                <Title xml:lang="deu">
                    <xsl:value-of select="$title"/>
                </Title>
                <Description xml:lang="deu">
                    <xsl:value-of select="$description"/>
                </Description>

                <Institution xml:lang="deu">
                    <xsl:value-of select="$institution"/>
                </Institution>
                <Environment xml:lang="deu">
                    <xsl:value-of select="$environment"/>
                </Environment>
                <Duration xml:lang="deu">
                    <xsl:value-of select="$duration"/>
                </Duration>
                <Period xml:lang="deu">
                    <xsl:value-of select="$period"/>
                </Period>
                <Conditions xml:lang="deu">
                    <xsl:value-of select="$conditions"/>
                </Conditions>
                <xsl:call-template name="cmd:Staff"/>
                <xsl:call-template name="cmd:Location"/>
                <xsl:call-template name="cmd:Sessions"/>
            </DGDEvent>
        </Components>
    </xsl:template>
</xsl:stylesheet>
