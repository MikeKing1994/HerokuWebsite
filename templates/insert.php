<html>
<body>
 
 
<?php
$con = mysql_connect("localhost","root","vjuhuj56");
if (!$con)
  {
  echo 'Could not connect: ';
  }
 
mysql_select_db("bucketlist", $con);
 
$sql="INSERT INTO tbl_user (user_name,user_username,user_passsword)
VALUES
('$_POST[inputName]','$_POST[inputEmail]','$_POST[inputPassword]')";
 
if (!mysql_query($sql,$con))
  {
  echo 'Error: query ';
  }
echo "1 record added";
 
mysql_close($con)
?>
</body>
</html>