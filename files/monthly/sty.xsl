<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
  <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
      <title>RSS | <xsl:value-of select="/rss/channel/title"/></title>
      <link rel='stylesheet' type='text/css' href='/sty.css?v=2024-07-21'/>
      <link rel='apple-touch-icon' sizes='57x57' href='/icons/apple-icon-57x57.png'/>
      <link rel='apple-touch-icon' sizes='60x60' href='/icons/apple-icon-60x60.png'/>
      <link rel='apple-touch-icon' sizes='72x72' href='/icons/apple-icon-72x72.png'/>
      <link rel='apple-touch-icon' sizes='76x76' href='/icons/apple-icon-76x76.png'/>
      <link rel='apple-touch-icon' sizes='114x114' href='/icons/apple-icon-114x114.png'/>
      <link rel='apple-touch-icon' sizes='120x120' href='/icons/apple-icon-120x120.png'/>
      <link rel='apple-touch-icon' sizes='144x144' href='/icons/apple-icon-144x144.png'/>
      <link rel='apple-touch-icon' sizes='152x152' href='/icons/apple-icon-152x152.png'/>
      <link rel='apple-touch-icon' sizes='180x180' href='/icons/apple-icon-180x180.png'/>
      <link rel='icon' type='image/png' sizes='192x192'  href='/icons/android-icon-192x192.png'/>
      <link rel='icon' type='image/png' sizes='32x32' href='/icons/favicon-32x32.png'/>
      <link rel='icon' type='image/png' sizes='96x96' href='/icons/favicon-96x96.png'/>
      <link rel='icon' type='image/png' sizes='16x16' href='/icons/favicon-16x16.png'/>
    </head>
    <body style='padding:20px'>
      <p>
        This is an RSS feed of the last year's issues of
        <a href='https://scientificcomputing.rs/monthly'>Scientific Computing in Rust Monthly</a>.
      </p>
      <xsl:for-each select="/rss/channel/item">
        <h1><a>
          <xsl:attribute name="href">
            <xsl:value-of select="link"/>
          </xsl:attribute>
          <xsl:value-of select="title"/>
        </a></h1>
        <xsl:value-of select="substring(pubDate, 0, 12)" />
        <div style='margin:10px 50px;padding:4px 25px;background-color:#F7AF90'>
          <xsl:copy-of select="description-html"/>
        </div>
      </xsl:for-each>
    </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
