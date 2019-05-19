<?php
error_reporting(E_ALL&~E_NOTICE);
$conn = mysqli_connect("localhost","root","","face_login");
 ?>
<!DOCTYPE html>
<html>
<head>
	<title>Face Attendance System</title>
	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="css/bootstrap-datetimepicker.min.css">
	<script type="text/javascript" src="js/jquery.js"></script>
	<script type="text/javascript" src="js/bootstrap.min.js"></script>
	<script type="text/javascript" src="js/bootstrap-datetimepicker.min.js"></script>
</head>
<body>
	<center>
		<h1>Face Attendance System</h1>
	</center><hr style="border-color:black;"><br><br>
	<div class="container">
		<div class="row">
			<div class="col-md-4">
				<h4>Add Member to Database</h4>
				<form class="form-horizontal" action="index.php" method="post" enctype="multipart/form-data">
  					<div class="form-group">
 	   					<input class="form-control" type="file" accept="image/jpeg" name="photo">
 	   					<div class="input-group">
 	   						<input type="text" class="form-control" name='name'id="name" placeholder="Name">
 	   						<div class="input-group-btn">
 	   							<button class="btn btn-default" type="submit">Submit</button>
 	   						</div>
 	   					</div>
 					</div>
				</form>

<?php 
if ($_POST['name']) {
	$query = "INSERT INTO face_id(name) values('".$_POST['name']."')";
	if (mysqli_query($conn,$query)) {
		$last_id=mysqli_insert_id($conn);
		$target = "known_face/";
		$targetf= $target.$last_id.".jpg";
		if(move_uploaded_file($_FILES["photo"]["tmp_name"],$targetf)){
					echo "Success";
				}else{
					echo "Error";
				}
}
}
 ?>
			</div>
			<div class="col-md-4">
				<h4>Member List</h4>
				<table class="table table-striped bg-light">
					<tr>
						<th>Member</th>
					</tr>
					<?php 
						$query = "SELECT * FROM face_id";
						$result = mysqli_query($conn,$query);
						if (mysqli_num_rows($result)>0) {
							while ($row=mysqli_fetch_assoc($result)) {
								echo "<tr><td>".$row['name']."</td></tr>";
							}
						}else{
							echo "<tr><td colspan='2'>NO DATA</td>";
						}
					 ?>
				</table>
			</div>
			<div class="col-md-4">
				<h4>Attendance List</h4>
				<form class="form-horizontal" id="form-attendance" action="index.php" method="GET">
  					<div class="form-group">
 	   					<div class="input-group">
 	   						<input type="date" class="form-control" name='date' id="date" placeholder="<?php if($_GET['date']){echo $_GET['date'];}else{echo 'Pick Date';}?>">
 	   						<div class="input-group-btn">
 	   							<button class="btn btn-default" type="submit">Submit</button>
 	   						</div>
 	   					</div>
						<table class="table table-striped bg-light">
							<tr>
								<th>Member</th>
								<th>Time</th>
							</tr>
							<?php 
									if ($_GET['date']) {
										$query = "SELECT * FROM date_attendance where date_log='".$_GET['date']."'";
										$result = mysqli_query($conn,$query);
										if (mysqli_num_rows($result)>0) {
											while ($row=mysqli_fetch_assoc($result)) {
												$q="SELECT  name FROM face_id where id='".$row['face_id']."'";
												$r=mysqli_query($conn,$q);
												$ro = mysqli_fetch_assoc($r);
											echo "<tr><td>".$ro['name']."</td><td>".$row['time_log']."</td></tr>";
											}
										}else{
										echo "<tr><td colspan='2'>NO DATA</td>";
									}
									}else{
										echo "<tr><td colspan='2'>NO DATA</td>";
									}
							 ?>
						</table>
 					</div>
				</form>
			</div>
		</div>
	</div>
</body>
</html>