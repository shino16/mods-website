<?
header('Content-Type: text/html; charset=UTF-8');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM organizers WHERE month=".($conn->real_escape_string($_GET['month']));
$result = $conn->query($sql);
if($result && $month_info = $result->fetch_assoc()){
	$nextmonth_info = $conn->query("SELECT * FROM organizers WHERE month>'".$month_info['month']."' ORDER BY month LIMIT 1")->fetch_assoc();
	$previousmonth_info = $conn->query("SELECT * FROM organizers WHERE month<'".$month_info['month']."' ORDER BY month DESC LIMIT 1")->fetch_assoc();
}else header('Location: organizers.php');
$sql = "SELECT * FROM countries";
$result = $conn->query($sql);
$countries=array();
while($row = $result->fetch_assoc()) {
	$countries[$row['code']]=$row['name'];
}
$conn->close();
function ord_of_num($num){
    switch($num%10) {
        case 1: return "st";
        case 2: return "nd";
        case 3: return "rd";
        default: return "th";
    }
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title><? echo $month_info['number'].ord_of_num($month_info['number']); ?> International Physics Olympiad</title>
</head>
<body>
<? $pagetype_timeline = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>
	<? if($previousmonth_info) echo '<a href="month_info.php?month='.$previousmonth_info['month'].'" class="pointer">&#9668;</a>'; ?>
	<a href="month_info.php?month=<? echo $month_info['month']; ?>" class="highlight"><? echo $month_info['number']; ?><sup><? echo ord_of_num($month_info['number']); ?></sup> IPHO <? echo $month_info['month']; ?></a>
	<? if($nextmonth_info) echo '<a href="month_info.php?month='.$nextmonth_info['month'].'" class="pointer">&#9658;</a>'; ?>
	</h2>
	<h3 class="hideprn">
	<a id="ctl00_CPH_Main_HyperLinkCountry" href="month_country.php?month=<? echo $month_info['month']; ?>">Country results</a> &bull;
	<a id="ctl00_CPH_Main_HyperLinkIndividual" href="month_individual.php?month=<? echo $month_info['month']; ?>">Individual results</a>
	<!-- &bull; <a id="ctl00_CPH_Main_HyperLinkStatistics" href="#">Statistics</a> -->
	</h3>
	<dl class="normal">
	<dt>General information</dt>
	<dd><? echo $month_info['city']?$month_info['city'].", ":""; ?><a href="country_info.php?code=<? echo $month_info['country']; ?>"><? echo $countries[$month_info['country']]; ?></a>
	<? if($month_info['homepage']!="") echo "(<a href=".$month_info['homepage']." target='_blank'>Home Page IPhO ".$month_info['month']."</a>),"; ?>
	<? echo $month_info['date']; ?> <? echo $month_info['month']; ?></dd>
	<? if($month_info['participatingcountries']) echo "<dd>Number of participating countries: ".$month_info['participatingcountries'].".</dd>"; ?>
	<? if($month_info['contestants']) echo "<dd>Number of contestants: ".$month_info['contestants'].".</dd>"; ?>
	<? if($month_info['gold'] + $month_info['silver'] + $month_info['bronze'] + $month_info['honourable'] > 0) { ?>
		<dt>Awards</dt>
		<dd>Gold medals: <? echo $month_info['gold']; ?>.<br />
		Silver medals: <? echo $month_info['silver']; ?>.<br />
		Bronze medals: <? echo $month_info['bronze']; ?>.<br />
		Honourable mentions: <? echo $month_info['honourable']; ?>.</dd>
		<? } ?>
	</dl>
</div>
<? include 'footer.php'; ?>
</body>
</html>
