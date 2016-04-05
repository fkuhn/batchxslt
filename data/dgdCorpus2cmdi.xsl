<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" 
    xmlns:cmd="http://www.clarin.eu/cmd/" exclude-result-prefixes="xd" version="2.0">

    <!-- dgdCorpus2cmdi 
    
    CHANGELOG
    
    
    
    v.2.1 
    - FIXED for-each now generates n Format instances.
    
    v2.0
    - added normalize-space for all selections
      
    -->

    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 25, 2014</xd:p>
            <xd:p><xd:b>Author:</xd:b> Florian Kuhn</xd:p>
            <xd:p/>
        </xd:desc>
    </xd:doc>

    <!-- NAMESPACE DEFINITIONS -->
    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- PARAMETER DEFINITIONS -->

    <!-- define parameters for CMDI header -->
    <xsl:param name="mdCreator" select="'DGD2CMDI'"/>
    <xsl:param name="mdCreationDate" select="current-date()"/>
    <xsl:param name="mdSelfLink" select="base-uri()"/>
    <xsl:param name="mdCollectionDisplayName" select="'AGD'"/>
    
    <!-- Clarin Profile ID that is assigned to each profile in the Clarin
    Component Registry (May 20th 2015).-->
    <xsl:param name="cmdProfile" select="'clarin.eu:cr1:p_1430905751614'"/>
    
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
    <xsl:param name="description"
        select="normalize-space(/Korpus/Korpus_Projekt_Kurzbeschreibung/text())"/>
    <xsl:param name="resourceType" select="normalize-space(/Korpus/Erstellungsprojekt/Typ/text())"/>
    <xsl:param name="modality"
        select="normalize-space(/Korpus/Korpusbestandteile[1]/Quellaufnahmen[1]/@Typ)"/>
    <xsl:param name="organisation"
        select="normalize-space(/Korpus/Erstellungsprojekt/Institut/text())"/>
    <xsl:param name="distributionType"
        select="/Korpus/Korpusbestandteile/Quellaufnahmen/Distribution/Zugänglichkeit/@Art"/>
   <!-- <xsl:param name="rightsHolder"
        select="normalize-space(/Korpus/Korpusbestandteile[1]/SE-Aufnahmen[1]/Distribution[1]/Zugänglichkeit[1]/Kontakt[1]/text())"/>-->
    <xsl:param name="projectTitle" select="normalize-space(/Korpus/Erstellungsprojekt/@Titel)"/>
    <xsl:param name="publicationYear"
        select="normalize-space(/Korpus/Erstellungsprojekt/Laufzeit/text())"/>
    <xsl:param name="languages"
        select="tokenize(normalize-space(/Korpus/Aufzeichnungsobjekte/Sprechereignisse/Basisdaten/Sprachen/text()),';')"/>
    <xsl:param name="format"
        select="/Korpus/Korpusbestandteile/SE-Aufnahmen/Digitale_Fassungen/Tontechnische_Daten/Format/text()"/>
    <xsl:param name="genre"
        select="normalize-space(/Korpus/Aufzeichnungsobjekte[1]/Sprechereignisse[1]/Basisdaten[1]/Arten[1]/text())"/>
    <xsl:param name="subject"
        select="normalize-space(/Korpus/Aufzeichnungsobjekte[1]/Sprechereignisse[1]/Inhalte[1]/Themen[1]/text())"/>
    <xsl:param name="keywords" select="tokenize(normalize-space(/Korpus/Deskriptoren/text()),';')"/>
    <xsl:param name="lastUpdate"
        select="normalize-space(/Korpus/Dokumentationsgeschichte/Update/@Datum)"/>

    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- DOCUMENT DEFINITIONS -->

    <!-- Define overall cmdi record structure -->
    <xsl:template match="/">
        <CMD xmlns="http://www.clarin.eu/cmd/" CMDVersion="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.clarin.eu/cmd/ http://catalog.clarin.eu/ds/ComponentRegistry/rest/registry/profiles/clarin.eu:cr1:p_1430905751614/xsd">
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
            <!-- <xsl:call-template name="cmd:ResourceProxyList"/>-->

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

    <!-- generate the Resource Tree Component for local linking of DGD Resources. -->
    <!-- TODO: Corpus-B-Tree -->
    <xsl:template name="cmd:ResourceTree">
        <CorpusTree>
        </CorpusTree>
    </xsl:template>
    
    <!-- generate an Keyword element for each tokenized keyword -->
    <xsl:template name="cmd:Keyword">
        <xsl:for-each select="for $counter in $keywords return $counter">
            <xsl:variable name="keyword" select="."/>
            <Keyword xml:lang="deu">
                <xsl:value-of select="normalize-space($keyword)"/>
            </Keyword>
        </xsl:for-each>
    </xsl:template>

    <!-- generate a Language element for each tokenized $languages value -->
    <xsl:template name="cmd:Languages">
        <xsl:for-each select="for $counter in $languages return $counter">
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
                <Name>
                    <xsl:value-of select="$name"/>
                </Name>
                <Title xml:lang="deu">
                    <xsl:value-of select="$title"/>
                </Title>
                <Description xml:lang="deu">
                    <xsl:value-of select="$description"/>
                </Description>
                <ResourceType xml:lang="deu">
                    <xsl:value-of select="$resourceType"/>
                </ResourceType>
                <!-- check if n occurences are possible and adjust selection -->
                <ResourceMediaType>
                    <xsl:value-of select="$modality"/>
                </ResourceMediaType>
                <Organisation xml:lang="deu">
                    <xsl:value-of select="$organisation"/>
                </Organisation>
                <xsl:for-each select="$distributionType">
                    <DistributionType xml:lang="deu">
                        <xsl:value-of select="."/>
                    </DistributionType>
                </xsl:for-each>
             <!--   <Copyright>
                    <xsl:value-of select="$rightsHolder"/>
                </Copyright>-->
                <ProjectTitle xml:lang="deu">
                    <xsl:value-of select="$projectTitle"/>
                </ProjectTitle>
                <PublicationYear>
                    <xsl:value-of select="$publicationYear"/>
                </PublicationYear>
                <xsl:call-template name="cmd:Languages"/>
                <xsl:for-each select="$format">
                    <DeliveryFormat xml:lang="deu">
                    <xsl:value-of select="."/>
                </DeliveryFormat>
                </xsl:for-each>
                <Genre xml:lang="deu">
                    <xsl:value-of select="$genre"/>
                </Genre>
                <Subject>
                    <xsl:value-of select="$subject"/>
                </Subject>
                <LastUpdate>
                    <xsl:value-of select="$lastUpdate"/>
                </LastUpdate>
                <Keywords>
                    <xsl:call-template name="cmd:Keyword"/>
                </Keywords>
            </DGDCorpus>
        </Components>
    </xsl:template>
</xsl:stylesheet>
