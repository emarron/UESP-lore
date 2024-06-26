### Data Cleaning

This section contains various scripts used to scrape, parse, sanitize, tag, and sort data into a usable format. The primary pipeline involves converting an HTML page into a JSON file with preserved context.

Directory cleaning_articles is divided into IP (Imperial Library) and UESP. These have various cleaning functions inside.

Directory cleaning_HTML has a UESP scraper, something to turn UESP HTML to JSON, something to (very generically) convert IP to JSON.

Directory cleaning_tes3conv_json is for handling JSON dumps of game data from tes3conv.

The `requirements.txt` will install various programs used in this section to clean data.


Example of cleaning data:


UESP HTML:
```html
<!DOCTYPE html>
<html class="client-nojs" lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
<title>Lore:ABCs for Barbarians - The Unofficial Elder Scrolls Pages (UESP)</title>
<script>document.documentElement.className = document.documentElement.className.replace( /(^|\s)client-nojs(\s|$)/, "$1client-js$2" );</script>
<script>(window.RLQ=window.RLQ||[]).push(function(){mw.config.set({"wgCanonicalNamespace":"Lore","wgCanonicalSpecialPageName":false,"wgNamespaceNumber":130,"wgPageName":"Lore:ABCs_for_Barbarians","wgTitle":"ABCs for Barbarians","wgCurRevisionId":2656323,"wgRevisionId":2656323,"wgArticleId":2306,"wgIsArticle":true,"wgIsRedirect":false,"wgAction":"view","wgUserName":null,"wgUserGroups":["*"],"wgCategories":["Lore Link-Resolved","Lore-Books"],"wgBreakFrames":false,"wgPageContentLanguage":"en","wgPageContentModel":"wikitext","wgSeparatorTransformTable":["",""],"wgDigitTransformTable":["",""],"wgDefaultDateFormat":"dmy","wgMonthNames":["","January","February","March","April","May","June","July","August","September","October","November","December"],"wgMonthNamesShort":["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],"wgRelevantPageName":"Lore:ABCs_for_Barbarians","wgRelevantArticleId":2306,"wgRequestId":"ecceacb913c4303aa0acb47c","wgIsProbablyEditable":true,"wgRelevantPageIsProbablyEditable":true,"wgRestrictionEdit":[],"wgRestrictionMove":[],"wgPreferredVariant":"en","wgMFExpandAllSectionsUserOption":false,"wgMFDisplayWikibaseDescriptions":{"search":false,"nearby":false,"watchlist":false,"tagline":false},"wgWikiEditorEnabledModules":{"toolbar":false,"preview":false,"publish":false},"wgPopupsShouldSendModuleToUser":true,"wgPopupsConflictsWithNavPopupGadget":false});mw.loader.state({"site.styles":"ready","noscript":"ready","user.styles":"ready","user":"ready","user.options":"loading","user.tokens":"loading","ext.EsoItemLink.styles":"ready","ext.EsoSkills.styles":"ready","ext.EsoSkills.styles2":"ready","ext.EsoSkills.baseStyles":"ready","ext.LegendCards.styles":"ready","mediawiki.legacy.shared":"ready","mediawiki.legacy.commonPrint":"ready","mediawiki.sectionAnchor":"ready","mediawiki.skinning.interface":"ready","mediawiki.skinning.content.externallinks":"ready","skins.monobook.styles":"ready","mediawiki.skinning.elements":"ready","mediawiki.skinning.content":"ready","skins.uespmonobook":"ready"});mw.loader.implement("user.options@0bhc5ha",function($,jQuery,require,module){mw.user.options.set([]);});mw.loader.implement("user.tokens@0qkqqui",function ( $, jQuery, require, module ) {
mw.user.tokens.set({"editToken":"+\\","patrolToken":"+\\","watchToken":"+\\","csrfToken":"+\\"});/*@nomin*/

});mw.loader.load(["ext.UespCustomCode.analytics","site","mediawiki.page.startup","mediawiki.user","mediawiki.hidpi","mediawiki.page.ready","mediawiki.searchSuggest","ext.uploadWizardUesp","ext.gadget.Discord","ext.popups","ext.EsoItemLink.scripts","ext.EsoSkills.scripts","ext.EsoSkills.scripts2","ext.EsoSkills.baseScripts","ext.LegendCards.scripts","ext.UespEsoData.resources"]);});</script>
<link rel="stylesheet" href="/w/load.php?debug=false&amp;lang=en&amp;modules=ext.EsoItemLink.styles%7Cext.EsoSkills.baseStyles%2Cstyles%2Cstyles2%7Cext.LegendCards.styles%7Cmediawiki.legacy.commonPrint%2Cshared%7Cmediawiki.sectionAnchor%7Cmediawiki.skinning.content%2Celements%2Cinterface%7Cmediawiki.skinning.content.externallinks%7Cskins.monobook.styles%7Cskins.uespmonobook&amp;only=styles&amp;skin=uespmonobook"/>
<script async="" src="/w/load.php?debug=false&amp;lang=en&amp;modules=startup&amp;only=scripts&amp;skin=uespmonobook"></script>
<!--[if IE 6]><link rel="stylesheet" href="/w/skins/UESP MonoBook/IE60Fixes.css?303" media="screen"/><![endif]--><!--[if IE 7]><link rel="stylesheet" href="/w/skins/UESP MonoBook/IE70Fixes.css?303" media="screen"/><![endif]--><!--[if IE 6]><link rel="stylesheet" href="/w/skins/uespmonobook/IE60Fixes.css?303" media="screen"/><![endif]--><!--[if IE 7]><link rel="stylesheet" href="/w/skins/uespmonobook/IE70Fixes.css?303" media="screen"/><![endif]-->
<meta name="ResourceLoaderDynamicStyles" content=""/>
<link rel="stylesheet" href="/w/load.php?debug=false&amp;lang=en&amp;modules=site.styles&amp;only=styles&amp;skin=uespmonobook"/>
<meta name="generator" content="MediaWiki 1.30.2"/>
<link rel="icon" type="image/png" href="https://images.uesp.net/favicon-16.png" sizes="16x16"/>
%%MORE SPAGHETTI%%

```

RESULT:
```json
{
    "Title": "ABCs for Barbarians",
    "Provenance": {
        "Article": "ABCs for Barbarians",
        "Writer": "",
        "Seen In": "Morrowind"
    },
    "Synopsis": "ABCs for Barbarians Picture book for barbarians",
    "Contents": "A is for Atronach . B is for Bungler's Bane . C is for Comberry .",
    "tags": [
        "Comberry",
        "Books",
        "Atronach",
        " ABCs for Barbarians Picture book for barbarians",
        "Seen In: Morrowind",
        "Bungler",
        "Article: ABCs for Barbarians"
    ]
}
```

IP HTML:
```html
<!DOCTYPE html><html
lang=en-US prefix="og: https://ogp.me/ns#">
<!-- Mirrored from www.imperial-library.info/content/abcs-barbarians by HTTrack Website Copier/3.x [XR&CO'2014], Mon, 24 Jun 2024 23:48:42 GMT -->
<!-- Added by HTTrack --><meta http-equiv="content-type" content="text/html;charset=UTF-8" /><!-- /Added by HTTrack -->
<head><style>img.lazy{min-height:1px}</style><link
rel=preload href=../wp-content/plugins/w3-total-cache/pub/js/lazyload.min.js as=script><meta
charset="UTF-8"><meta
name="viewport" content="width=device-width, initial-scale=1"><link
rel=profile href=https://gmpg.org/xfn/11><title>ABCs for Barbarians &mdash; The Imperial Library</title><meta
name="description" content="A book for babies... or barbarians"><meta
name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large"><link
rel=canonical href=abcs-barbarians.html><meta
property="og:locale" content="en_US"><meta
property="og:type" content="article"><meta
property="og:title" content="ABCs for Barbarians &mdash; The Imperial Library"><meta
property="og:description" content="A book for babies... or barbarians"><meta
property="og:url" content="https://www.imperial-library.info/content/abcs-barbarians"><meta
property="og:site_name" content="The Imperial Library"><meta
%%MORE SPAGHETTI%%
```

RESULT
```json
{
    "Title": "ABCs for Barbarians",
    "Tags": [
        "Book"
    ],
    "Released In": [
        "ESO: Morrowind"
    ],
    "Category": "manuals & instructions",
    "Author": "Anonymous",
    "Synopsis": "A book for babies... or barbarians",
    "Contents": "A is for Atronach.\nB is for Bungler’s Bane.\nC is for Comberry."
}
```

