<?
header('Content-Type: text/html; charset=UTF-8');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM organizers WHERE month=".($conn->real_escape_string($_GET['month']));
$result = $conn->query($sql);
if($result && $month_info = $result->fetch_assoc()) {
	$nextmonth_info = $conn->query("SELECT * FROM organizers WHERE month>'".$month_info['month']."' ORDER BY month LIMIT 1")->fetch_assoc();
	$previousmonth_info = $conn->query("SELECT * FROM organizers WHERE month<'".$month_info['month']."' ORDER BY month DESC LIMIT 1")->fetch_assoc();
} else header('Location: organizers.php');
$sql = "SELECT * FROM countries";
$result = $conn->query($sql);
$countries = array();
$medals = array();
while($row = $result->fetch_assoc()) {
	$countries[$row['code']] = $row['name'];
	$medals[$row['code']] = 0;
}
$conn->close();
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM estudiante WHERE month=".$month_info['month'];
if($result = $conn->query($sql)) {
	while($row = $result->fetch_assoc()) {
		switch($row['medal']) {
			case 1: $medals[$row['country']] += 1000; break;
			case 2: $medals[$row['country']] += 100; break;
			case 3: $medals[$row['country']] += 10; break;
			case 4: $medals[$row['country']] += 1; break;
		}
	}
}
arsort($medals);
$conn->close();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title>IPhO <? echo $month_info['month'] ?> - Individual Results</title>
</head>
<body>
<? $pagetype_timeline = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>
	<? if($previousmonth_info) echo '<a href="month_country.php?month='.$previousmonth_info['month'].'" class="pointer">&#9668;</a>'; ?>
	<a href="month_info.php?month=<? echo $month_info['month']; ?>"><? echo $month_info['number']; ?><sup>th</sup> IPHO <? echo $month_info['month']; ?></a>
	<? if($nextmonth_info) echo '<a href="month_country.php?month='.$nextmonth_info['month'].'" class="pointer">&#9658;</a>'; ?>
	</h2>
	<h3>
	<a class="highlight" href="month_country.php?month=<? echo $month_info['month']; ?>">Country results</a> &bull;
	<a class="hideprn" href="month_individual.php?month=<? echo $month_info['month']; ?>">Individual results</a>
	<!-- &bull; <a class="hideprn" href="month_statistics.php?month=<? echo $month_info['month']; ?>">Statistics</a> -->
	</h3>
	<table>
	<thead>
	<tr>
	<th rowspan="2">Country</th>
	<th rowspan="2">Rank</th>
	<th colspan="4">Awards</th>
	</tr>
	<tr>
	<th title="Gold medal">G</th><th title="Silver medal">S</th><th title="Bronze medal">B</th><th title="Honourable mention">HM</th></tr>
	</thead><tbody>
	<?
	$i = 1;
	foreach($medals as $code => $medalx) {
	    echo "<tr><td><a href='country_individual.php?code=".$code."'>".$countries[$code]."</a></td><td>".$i."</td><td>".($medalx / 1000 % 10)."</td><td>".($medalx / 100 % 10)."</td><td>".($medalx / 10 % 10)."</td><td>".($medalx % 10)."</td></tr>";
	    $i++;
	}
	?>
	</tbody>
	</table>
	<div>
		Results may not be complete and may include mistakes.
		Please send relevant information to the webmaster:
		<a href="mailto:webmaster@ipho-official.org">webmaster@ipho-unofficial.org</a>.
	</div>
</div>
<? include 'footer.php'; ?>
</body>
</html>