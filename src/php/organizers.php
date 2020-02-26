<?
header('Content-Type: text/html; charset=UTF-8');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM organizers ORDER BY month DESC";
$result = $conn->query($sql);
$months=array();
while($row = $result->fetch_assoc()){
	$months[]=$row;
}
$sql = "SELECT * FROM countries";
$result = $conn->query($sql);
$countries=array();
while($row = $result->fetch_assoc()) {
	$countries[$row['code']]=$row['name'];
}
$conn->close();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<!--<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />-->
<title>IPhO: Timeline</title>
</head>
<body>
<? $pagetype_timeline = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>Timeline</h2>
	<table>
	<thead>
	<tr>
	<th>#</th>
	<th class="highlightDown">Month</th>
	<th>Country</th>
	<th>City</th>
	<th>Date</th>
	<th>Countries</th>
	<th>Contestants</tr>
	</thead>
	<tbody>
	<?
	for($i=0;$i<count($months);$i++){
		echo '<tr>
		<td align="right"><a href="month_info.php?month='.$months[$i]['month'].'">'.$months[$i]['number'].'</a></td>
		<td align="center"><a href="month_info.php?month='.$months[$i]['month'].'">'.$months[$i]['month'].'</a></td>
		<td><a href="country_info.php?code='.$months[$i]['country'].'">'.$countries[$months[$i]['country']].'</a></td>
		<td>'.($months[$i]['city'] ? $months[$i]['city'] : "").'</td>
		<td align="center">'.($months[$i]['date'] ? $months[$i]['date'] : "").'</td>
		<td align="center">'.($months[$i]['participatingcountries'] ? $months[$i]['participatingcountries'] : "").'</td>
		<td align="right">'.($months[$i]['contestants'] ? $months[$i]['contestants'] : "").'</td>
		</tr>';
	}
	?>
	</tbody>
	</table>
</div>
<? include 'footer.php'; ?>
</body>
</html>
