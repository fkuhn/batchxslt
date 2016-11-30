<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:cmd="http://www.clarin.eu/cmd/" exclude-result-prefixes="xd" version="2.0">

    <!-- 
    
    ACHTUNG: Default-namespaces werden nicht als attribut generiert xmlns:    
    
    dgdCorpus2cmdi 
    Ueberarbeitung der XSL Transformation Stylesheets zur Abdeckung der CLARIN VLO Facets.
    Zweite Version im Maerz 2016
   
    Jede CMD Metafile glieder sich in drei Inhaltsbereiche:
    1. Header
    2. Resources
    3. Components
    
    *Header* enthält Metadaten zu den Metadatendateien und untergliedern sich in 
    a) MdCreator: Bezeichner des Tools, das das Metafile genierte, e.g. dgd2cmdi
    b) MdCreationDate: Das Datum der Generierung der Metafile. Wird direkt erzeugt.
    c) MdSelfLink: Der Selbstverweis mittels Persistent Identifier (e.g. http://hdl.handle.net/10932/00-01B8-EF34-596D-DF01-7)
    d) MdProfile: Das von der Metafile verwendete Profil aus der Clarin Component Registry. Für diesen Stylesheet also: clarin.eu:cr1:p_1455633534543
    e) MdCollectionDisplayName: Ein Bezeichner für das Gesamtverzeichnis, zu dem die Resource zählt, also "AGD"
    
    *Resource* enthält Angaben zu mit der Resource assozierte weitere Resourcen. Bei einer Korpus-Metafile sind dies prinzipiell alle dem Korpus zugerechnete
    Resourcen. Für die Resourcen der AGD/DGD sind dies im CLARIN Kontext konvertierten Event-Metafiles, Audio bzw. Media-Files sowie Transkripte.
    Die originären Speaker-Metafiles werden nicht übernommen, aber wesentliche Informationen aus diesen Dateien werden in die passenden Session-Abschnitte
    einer Event-Metafile eingefügt - also dort, wo der in der Speaker-File aufgeführte Sprecher teil genommen hat.
    a) ResourceProxyList: Liste der bereits oben beschriebenen beteiligten Resourcen.
        1.  ResourceProxy ist das Subelement von a), ist ein komplexes Element und beschreibt einen Verweis auf eine Resource .
            Sein Attribut "id" besitzt eindeutigen, internen Bezeichnerwert (keine PID). Es hat wiederum die Kinder
            a) ResourceType: besitzt das Attribut mimetype (e.g. "application/xml") sowie ein Textvalue, das die Art der Resource beschreibt. Default ist "Resource".
            b) ResourceRef: URI zum (physikalischen) Ort der Resource. Bei AGD Resourcen wird ein RESTful Ausdruck verwendet, um sie über das Webinterface der AGD einzubinden.    
    b) JournalFileProxyList: Liste der ?. Derzeit keine Nutzung. Dokumentation nicht vorhanden.
    c) ResourceRelationList: Liste von Relationsdefinitionen zwischen den beteiligten Resourcen. Derzeit keine Nutzung. Dokumenation nicht vorhanden.
    
    *Components* enthält die Gesamtheit der konkreten Informationen eines Metafiles, die nicht wiederum Metadaten sind.  
    
    *Resourcen bzgl CMDI 1.1*
    
    https://www.clarin.eu/content/cmdi-tutorial-september-2012
    https://svn.clarin.eu/metadata/branches/cmdi-1.1/
    **XSLT Stylesheets**
    https://svn.clarin.eu/metadata/branches/cmdi-1.1/toolkit/xslt/
    
    *Weitere Infos* 
    
    https://pure.knaw.nl/ws/files/470440/Metadata_Test_Create_LREC2010_def-v2.pdf
    
    http://www.clarin.eu/sites/default/files/Erhard_Hinrichs_Survey_of_Resources_and_Tools_v2.pdf
    -->


    <!-- 
       ***********************
        Parameter Definitions
       ***********************
       
    -->

    <!-- NAMESPACE DEFINITIONS -->
    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- PARAMETER DEFINITIONS -->

    <!-- define parameters for CMDI header -->
    <xsl:param name="mdCreator" select="'DGD2CMDI'"/>
    <xsl:param name="mdCreationDate" select="current-date()"/>
    <xsl:param name="mdSelfLink" select="base-uri()"/>
    <xsl:param name="mdCollectionDisplayName" select="'AGD'"/>

    <!-- Clarin Profile ID that is assigned to each profile in the Clarin
    Component Registry (March 2th 2016).-->
    <xsl:param name="cmdProfile" select="'clarin.eu:cr1:p_1455633534543'"/>

    <!-- determine lists of dependent resources-->
    <xsl:param name="corpusname" select="tokenize(base-uri(), '-')[0]"/>

    <!-- Resource Proxies -->
    <xsl:param name="resourceProxyList" select="''"/>
    <xsl:param name="journalFileProxyList" select="''"/>
    <xsl:param name="resourceRelationList" select="''"/>

    <!-- define parameters for corpus components according vlo search facets -->
    <!-- due to the ambiguous definitions of elements in the dgd metadata schema, absolute xpath expressions are used -->

    <xsl:param name="name" select="normalize-space(/Korpus/Name/text())"/>
    <xsl:param name="title" select="normalize-space(/Korpus/Sonstige_Bezeichnungen/text())"/>
    <xsl:param name="collection" select="'AGD'"/>
    <xsl:param name="projectTitle" select="normalize-space(/Korpus/Erstellungsprojekt/@Titel)"/>
    <xsl:param name="description"
        select="normalize-space(/Korpus/Korpus_Projekt_Kurzbeschreibung/text())"/>
    <xsl:param name="resourceType" select="normalize-space(/Korpus/Erstellungsprojekt/Typ/text())"/>
    <xsl:param name="media"
        select="normalize-space(/Korpus/Korpusbestandteile[1]/Quellaufnahmen[1]/@Typ)"/>
    <xsl:param name="modality"
        select="/Korpus/Aufzeichnungsobjekte[1]/Sprechereignisse[1]/Basisdaten[1]/Mediale_Realisierung[1]/text()"/>
    <xsl:param name="organisation"
        select="normalize-space(/Korpus/Erstellungsprojekt/Institut/text())"/>
    <xsl:param name="distributionType"
        select="/Korpus/Korpusbestandteile/Quellaufnahmen/Distribution/@Stelle"/>
    <xsl:param name="availability"
        select="/Korpus/Korpusbestandteile/Quellaufnahmen/Distribution/Zugänglichkeit/@Art"/>
    <xsl:param name="rightsHolder"
        select="normalize-space(/Korpus/Korpusbestandteile[1]/SE-Aufnahmen[1]/Distribution[1]/Zugänglichkeit[1]/Kontakt[1]/text())"/>
    <xsl:param name="license" select="'CLARIN RES+BY+NC+NORED'"/>
    <xsl:param name="publicationYear"
        select="normalize-space(/Korpus/Erstellungsprojekt/Laufzeit/text())"/>
    <xsl:param name="languages"
        select="tokenize(normalize-space(/Korpus/Aufzeichnungsobjekte/Sprechereignisse/Basisdaten/Sprachen/text()), ';')"/>
    <xsl:param name="format"
        select="/Korpus/Korpusbestandteile/SE-Aufnahmen/Digitale_Fassungen/Tontechnische_Daten/Format/text()"/>
    <xsl:param name="genre"
        select="normalize-space(/Korpus/Aufzeichnungsobjekte[1]/Sprechereignisse[1]/Basisdaten[1]/Arten[1]/text())"/>
    <xsl:param name="subject"
        select="normalize-space(/Korpus/Aufzeichnungsobjekte[1]/Sprechereignisse[1]/Inhalte[1]/Themen[1]/text())"/>
    <xsl:param name="keywords" select="tokenize(normalize-space(/Korpus/Deskriptoren/text()), ';')"/>
    <xsl:param name="lastUpdate"
        select="normalize-space(/Korpus/Dokumentationsgeschichte/Update/@Datum)"/>

    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- DOCUMENT DEFINITIONS -->

    <!-- Define overall cmdi record structure -->
    <xsl:template match="/">
        <CMD xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" CMDVersion="1.1"
            xsi:schemaLocation="http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1455633534543/xsd"
            xmlns="http://www.clarin.eu/cmd/">

            <!-- 
                  ************************
                    Build Header section
                  ************************
            -->
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

            <!-- 
               ************************* 
                Build Resources Section
               *************************
            -->
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

    <!-- 
               *******************
                Build Components
               *******************
            -->

    <!-- generate an Keyword element for each tokenized keyword -->
    <xsl:template name="cmd:Keyword">
        <xsl:for-each
            select="
                for $counter in $keywords
                return
                    $counter">
            <xsl:variable name="keyword" select="."/>
            <Keyword xml:lang="deu">
                <xsl:value-of select="normalize-space($keyword)"/>
            </Keyword>
        </xsl:for-each>
    </xsl:template>

    <!-- generate a Language element for each tokenized $languages value -->
    <xsl:template name="cmd:Languages">
        <xsl:for-each
            select="
                for $counter in $languages
                return
                    $counter">
            <xsl:variable name="language" select="."/>
            <Language xml:lang="deu">
                <xsl:value-of select="$language"/>
            </Language>
        </xsl:for-each>
    </xsl:template>

    <!-- generate the output cmdi metadata file -->
    <xsl:template name="cmd:Components">
        <Components>
            <DGDCorpus>
                <ID>
                    <!-- INSERT HANDLE.NET PID HERE -->
                </ID>
                <Collection>
                    <xsl:value-of select="$collection"/>
                </Collection>
                <ProjectTitle xml:lang="deu">
                    <xsl:value-of select="$projectTitle"/>
                </ProjectTitle>
                <Name>
                    <xsl:value-of select="$name"/>
                </Name>
                <!--<Title xml:lang="deu">
                    <xsl:value-of select="$title"/>
                </Title>-->
                <Institution xml:lang="deu">
                    <xsl:value-of select="$organisation"/>
                </Institution>
                <RightsHolder>
                    <xsl:value-of select="$rightsHolder"/>
                </RightsHolder>
                <PublicationYear>
                    <xsl:value-of select="$publicationYear"/>
                </PublicationYear>
                <Description xml:lang="deu">
                    <xsl:value-of select="$description"/>
                </Description>
                <TemporalCoverage xml:lang="deu">
                    <xsl:value-of
                        select="normalize-space(/Korpus/Erstellungsprojekt/Laufzeit/text())"/>
                </TemporalCoverage>
                <License><xsl:value-of select="$license"/></License>
                <ResourceType xml:lang="deu">
                    <xsl:value-of select="$resourceType"/>
                </ResourceType>
                <ResourceMediaType>
                    <xsl:value-of select="$media"/>
                </ResourceMediaType>
                <xsl:for-each select="$distributionType">
                    <DistributionType xml:lang="deu">
                        <xsl:value-of select="."/>
                    </DistributionType>
                </xsl:for-each>

                <Continent>
                    <!-- No Continent Values used so far -->
                </Continent>
                <Country xml:lang="deu">
                    <xsl:value-of
                        select="/Korpus/Aufzeichnungsobjekte[1]/Ereignisse_Basisdaten[1]/Länder_Regionen_Orte[1]/text()"
                    />
                </Country>
                <xsl:call-template name="cmd:Languages"/>
                <xsl:for-each select="$format">
                    <DeliveryFormat xml:lang="deu">
                        <xsl:value-of select="."/>
                    </DeliveryFormat>
                </xsl:for-each>
                <Genre xml:lang="deu">
                    <xsl:value-of select="$genre"/>
                </Genre>
                <Modality xml:lang="deu">
                    <xsl:value-of select="$modality"/>
                </Modality>
                <Subject>
                    <xsl:value-of select="$subject"/>
                </Subject>
                
                <LastUpdate>
                    <xsl:value-of select="$lastUpdate"/>
                </LastUpdate>
                <ComponentProfile>
                    <xsl:value-of select="normalize-space($cmdProfile)"/>
                </ComponentProfile>
                <Text xml:lang="deu"/>
                <SelfLink>
                    <xsl:value-of select="normalize-space($mdSelfLink)"/>
                </SelfLink>
                <Keywords>
                    <xsl:call-template name="cmd:Keyword"/>
                </Keywords>
                
            </DGDCorpus>
        </Components>
    </xsl:template>
</xsl:stylesheet>
