<body class="ltr">
<!-- POPUPKART -->
<script type="text/javascript" src="http://www.mtgnews.pl/forum/scripts/wz_tooltip/wz_tooltip.js"></script>
<!-- POPUPKART END -->

<script type="text/javascript" src="http://www.mtgnews.pl/forum/scripts/wz_tooltip/wz_tooltip.js"></script>
<script type="text/javascript" language="JavaScript">
var karta = "Fetid Pools";
karta = karta.replace( new RegExp( " ", "g" ), "%20" );
karta = karta.replace(/'/g,'');
karta = karta.replace( new RegExp( "&#39;", "g" ), "'" );

var randomname1=Math.floor(Math.random()*9001);
var randomname2=Math.floor(Math.random()*501);

var tipId = karta + randomname1 + randomname2;
tipId = tipId.replace( new RegExp( "'", "g" ), "" );

document.write('<a href="http://gatherer.wizards.com/Pages/Card/Details.aspx?name=Fetid Pools" target="_blank" onmouseover="TagToTip(\''+ tipId +'\',FADEIN, 400, FADEOUT, 400, BGCOLOR, \'#000000\', FONTCOLOR, \'#ffffff\', BORDERCOLOR, \'#000000\')" onmouseout="UnTip()">Fetid Pools</a>');
document.write('<span id="'+ tipId +'" style="visibility:hidden; position:absolute;"><img src="http://gatherer.wizards.com/Handlers/Image.ashx?type=card&name='+karta+'"></span>');
</script>
</body>
