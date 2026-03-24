<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela</title>
    <style>
        table,tr,td{
            border: solid black 1px;
        }
    </style>
</head>
<body>
    <?php
    $conn = new mysqli('localhost','root','','auta');
    $q = 'SELECT * FROM pracownicy';
    $res = $conn -> query($q);

    echo "<table>";
    while($row = $res -> fetch_row()){
        echo "<tr>
        <td>$row[0]</td>
        <td>$row[1]</td>
        <td>$row[2]</td>
        <td>$row[3]</td>
        <td>$row[4]</td>
        <td>$row[5]</td>
        <td>$row[6]</td>
        </tr>";
    }
    echo "</table>";
    ?>
</body>
</html>