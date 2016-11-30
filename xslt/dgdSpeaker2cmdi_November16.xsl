<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:cmd="http://www.clarin.eu/cmd/" exclude-result-prefixes="xs xd" version="2.0">
    
    <!-- 
    
    Da sich die extrahierten Speaker-Informationen zwischen den beiden Stylesheet Revisionen (May 15 vs. March 16) nicht geändert haben, 
    werden keine Änderungen an diesem Stylesheet durchgeführt. 
    
    
    CHANGELOG
    
    2.1:a
    - renamed Occupation to Profession 
    - Documentation Attribute convention: using XPATH expression to values in original german markup (in cmdi profile)
    - 
    CHANGELOG v2
    
    * FIXED: DateOfBirth not addressed correctly. 
    
    
    -->
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Dec 22, 2014</xd:p>
            <xd:p><xd:b>Author:</xd:b> kuhn</xd:p>
            <xd:p/>
        </xd:desc> 
    </xd:doc>

    <!-- NAMESPACE DEFINITIONS -->
    <xsl:namespace-alias stylesheet-prefix="cmd" result-prefix="#default"/>

    <!-- define parameters for CMDI header -->
    <xsl:param name="mdCreator" select="'DGD2CMDI'"/>
    <xsl:param name="mdCreationDate" select="current-date()"/>
    <xsl:param name="mdSelfLink" select="base-uri()"/>
    <xsl:param name="mdCollectionDisplayName" select="'AGD'"/>
    <xsl:param name="cmdProfile" select="'clarin.eu:cr1:p_1407745712074'"/>

    <!-- Resource Proxies parameters-->
    <xsl:param name="resourceProxyList" select="' '"/>
    <xsl:param name="journalFileProxyList" select="' '"/>
    <xsl:param name="resourceRelationList" select="''"/>

    <!-- Events the Speaker is participating -->
    <!-- /Sprecher/In_Sprechereignis/SE-Kennung -->

<!--    <Basisdaten>
        <Sonstige_Bezeichnungen>FOLK_BERU_01_T01</Sonstige_Bezeichnungen>
        <Name>Anonym</Name>
        <Früherer_Name>Anonym</Früherer_Name>
        <Pseudonym>Michael Lengefeld</Pseudonym>
        <Geschlecht>Männlich</Geschlecht>
        <Geburtsdatum>
            <YYYY-MM-DD>9999-01-01</YYYY-MM-DD>
            <Anmerkungen>Nicht dokumentiert</Anmerkungen>
        </Geburtsdatum>
        <Auffällige_Merkmale>Nicht dokumentiert</Auffällige_Merkmale>
        <Bildungsabschluss>Nicht dokumentiert</Bildungsabschluss>
        <Berufe>Schüler (Berufsschule)</Berufe>
        <Ethnische_Zugehörigkeit>Nicht dokumentiert</Ethnische_Zugehörigkeit>
        <Gruppenzugehörigkeit>Nicht dokumentiert</Gruppenzugehörigkeit>
        <Staatsangehörigkeit>Nicht dokumentiert</Staatsangehörigkeit>
        <Weitere_biographische_Daten>Vgl. Ortsdaten</Weitere_biographische_Daten>
        <Zuschreibungen>Nicht dokumentiert</Zuschreibungen>
        <Sigle_in_Transkripten>ML</Sigle_in_Transkripten>
        <Anmerkungen/>
        
    </Basisdaten>-->
    <xsl:template name="cmd:BaseData">
        <Name><xsl:value-of select="/Sprecher/Basisdaten[1]/Name[1]/text()"></xsl:value-of></Name>
        <Alias><xsl:value-of select="/Sprecher/Basisdaten[1]/Pseudonym[1]/text()"></xsl:value-of></Alias>
        <TranscriptID><xsl:value-of select="/Sprecher/Basisdaten[1]/Sigle_in_Transkripten[1]/text()"></xsl:value-of></TranscriptID>
        <Sex xml:lang="deu"><xsl:value-of select="/Sprecher/Basisdaten[1]/Geschlecht[1]/text()"></xsl:value-of></Sex>
        <DateOfBirth><xsl:value-of select="/Sprecher/Basisdaten[1]/Geburtsdatum[1]/YYYY-MM-DD/text()"></xsl:value-of></DateOfBirth>
        <Education xml:lang="deu"><xsl:value-of select="/Sprecher/Basisdaten[1]/Bildungsabschluss[1]/text()"></xsl:value-of></Education>
        <Profession xml:lang="deu"><xsl:value-of select="/Sprecher/Basisdaten[1]/Berufe/text()"></xsl:value-of></Profession>
        <Ethnicity xml:lang="deu"><xsl:value-of select="/Sprecher/Basisdaten[1]/Ethnische_Zugehörigkeit[1]/text()"></xsl:value-of></Ethnicity>
        <Nationality xml:lang="deu"><xsl:value-of select="/Sprecher/Basisdaten[1]/Staatsangehörigkeit[1]/text()"></xsl:value-of></Nationality>
    </xsl:template>
    
    <!-- Location Data-->
    <xsl:template name="cmd:LocationData">
        <!-- TODO: rework geolocation -->
        <LocationData>
            <xsl:for-each select="/Sprecher/Ortsdaten">
                <Location>
                    <LocationType xml:lang="deu"><xsl:value-of select="./@Typ"></xsl:value-of></LocationType>
                    <Grid><xsl:value-of select="./Koordinaten/Planquadrat/text()"></xsl:value-of></Grid>
                    <Country xml:lang="deu"><xsl:value-of select="./Land/text()"></xsl:value-of></Country>
                    <Region xml:lang="deu"><xsl:value-of select="./Region/text()"></xsl:value-of></Region>
                    <Place xml:lang="deu"><xsl:value-of select="./Ortsname/text()"></xsl:value-of></Place>
                </Location>
            </xsl:for-each>
        </LocationData>
    </xsl:template>
    <!-- TOODO: Use Geolocation Tmplate by Peter Fischer -->
<!--        <xsl:template name="cmd:GeoLocation">
        <GeoLocation>
            <Vertex>
                
            </Vertex>
            <Latitude>
                
            </Latitude>
            <Longitude>
                
            </Longitude>
        </GeoLocation>
        </xsl:template>-->
    
<!-- ****GeoLocalization Templates by Peter Fischer. (XSLT 1.0 port) **** -->
    
    <xsl:template name="cmd:GeoLocalization" match="./Koordinaten" mode="GeoLocalization">
        <xsl:variable name="srcGrids" select="./Planquadrat/text()"/>
        
        <xsl:call-template name="cmd:extractCoordinates">
            <xsl:with-param name="gridsquares" select="$srcGrids"/>
        </xsl:call-template>
    </xsl:template>
    
    <xsl:variable name="componentIdGeoLocalization" select="'clarin.eu:cr1:c_1361876010667'"/>
    <xsl:template name="cmd:extractCoordinates">
        <xsl:param name="minx" select="''"/>
        <xsl:param name="miny" select="''"/>
        <xsl:param name="maxx" select="''"/>
        <xsl:param name="maxy" select="''"/>
        <xsl:param name="gridsquares" select="''"/>
        
        <xsl:variable name="digits" select="'0123456789'"/>
        
        <xsl:choose>
            <xsl:when test="$gridsquares = 'Nicht dokumentiert'"/>
            <!-- recursion terminator -->
            <xsl:when test="$gridsquares = ''">
                <xsl:choose>
                    <xsl:when test="$minx = '' or $miny = '' or $maxx = '' or $maxy = ''"/>
                    <xsl:otherwise>
                        <GeoLocalization ComponentId="{$componentIdGeoLocalization}">
                            <xsl:call-template name="constructPolygonFromSquare">
                                <xsl:with-param name="x1" select="$minx"/>
                                <xsl:with-param name="y1" select="$miny"/>
                                <xsl:with-param name="x2" select="$maxx + 1"/>
                                <xsl:with-param name="y2" select="$maxy + 1"/>
                            </xsl:call-template>
                        </GeoLocalization>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <!-- match \d{4} -->
            <xsl:when test="contains($digits,substring($gridsquares,1,1)) and contains($digits,substring($gridsquares,2,1)) and contains($digits,substring($gridsquares,3,1)) and contains($digits,substring($gridsquares,4,1))">
                <xsl:variable name="x" select="number(substring($gridsquares,3,2))"/>
                <xsl:variable name="y" select="number(substring($gridsquares,1,2))"/>
                
                <xsl:call-template name="cmd:extractCoordinates">
                    <xsl:with-param name="minx">
                        <xsl:choose>
                            <xsl:when test="$minx = '' or $x &lt; $minx">
                                <xsl:value-of select="$x"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$minx"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="miny">
                        <xsl:choose>
                            <xsl:when test="$miny = '' or $y &lt; $miny">
                                <xsl:value-of select="$y"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$miny"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="maxx">
                        <xsl:choose>
                            <xsl:when test="$maxx = '' or $x &gt; $maxx">
                                <xsl:value-of select="$x"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$maxx"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="maxy">
                        <xsl:choose>
                            <xsl:when test="$maxy = '' or $y &gt; $maxy">
                                <xsl:value-of select="$y"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$maxy"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                    <xsl:with-param name="gridsquares" select="substring($gridsquares,5)"/>
                </xsl:call-template>
            </xsl:when>
            <!-- chop first char -->
            <xsl:otherwise>
                <xsl:call-template name="cmd:extractCoordinates">
                    <xsl:with-param name="minx" select="$minx"/>
                    <xsl:with-param name="miny" select="$miny"/>
                    <xsl:with-param name="maxx" select="$maxx"/>
                    <xsl:with-param name="maxy" select="$maxy"/>
                    <xsl:with-param name="gridsquares" select="substring($gridsquares,2)"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="constructPolygonFromSquare">
        <xsl:param name="x1"/>
        <xsl:param name="y1"/>
        <xsl:param name="x2"/>
        <xsl:param name="y2"/>
        
        <Vertex>
            <xsl:call-template name="convertCoordinates">
                <xsl:with-param name="x" select="$x1"/>
                <xsl:with-param name="y" select="$y1"/>
            </xsl:call-template>
        </Vertex>
        <Vertex>
            <xsl:call-template name="convertCoordinates">
                <xsl:with-param name="x" select="$x1"/>
                <xsl:with-param name="y" select="$y2"/>
            </xsl:call-template>
        </Vertex>
        <Vertex>
            <xsl:call-template name="convertCoordinates">
                <xsl:with-param name="x" select="$x2"/>
                <xsl:with-param name="y" select="$y2"/>
            </xsl:call-template>
        </Vertex>
        <Vertex>
            <xsl:call-template name="convertCoordinates">
                <xsl:with-param name="x" select="$x2"/>
                <xsl:with-param name="y" select="$y1"/>
            </xsl:call-template>
        </Vertex>
    </xsl:template>
     
    <xsl:template name="convertCoordinates">
        <xsl:param name="x"/>
        <xsl:param name="y"/>
        
        <Latitude>
            <xsl:value-of select="56 - ($y - 1) div 6"/>
        </Latitude>
        <Longitude>
            <xsl:value-of select="6 + ($x - 1) div 4"/>
        </Longitude>
    </xsl:template>
    
    
<!-- ***END OF GeoLocalization Template -->
    <!-- Language Data. For all "Sprachkenntnisse", check if current element "." is native language. -->
    <xsl:template name="cmd:LanguageData">
        <LanguageData>
            <xsl:for-each select="/Sprecher/Sprachdaten/Sprachkenntnisse">
                <xsl:if test="./Sprachstatus = 'Muttersprache'">
                    <NativeLanguage xml:lang="deu"><xsl:value-of select="./@Sprachname"></xsl:value-of></NativeLanguage>
                </xsl:if>
                <xsl:if test="./Sprachstatus != 'Muttersprache'">
                    <Language xml:lang="deu"><xsl:value-of select="./@Sprachname"></xsl:value-of></Language>
                </xsl:if>
            </xsl:for-each>
        </LanguageData>
        
    </xsl:template>
    <!-- Events the speaker occurs in. Iterate over all "SE-Kennung" elements -->
    <xsl:template name="cmd:InEvents">
        <InEvents>
        <xsl:for-each select="/Sprecher/In_Sprechereignis/SE-Kennung">
            <EventSession>
                <xsl:value-of select="./text()"/>
            </EventSession>
        </xsl:for-each>
        </InEvents>
    </xsl:template>
    
   <!-- Component and call of sub-templates -->
    <xsl:template name="cmd:Components">
        <Components>
        <xsl:call-template name="cmd:InEvents"/>
        <xsl:call-template name="cmd:BaseData"/>
        <xsl:call-template name="cmd:LocationData"/>
        <xsl:call-template name="cmd:LanguageData"/>
        </Components>
    </xsl:template> 

    <!-- Build Header Information and Call component template -->
    <xsl:template match="/">
        <CMD CMDVersion="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
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

</xsl:stylesheet>
