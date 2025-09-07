<!DOCTYPE html>
<html lang="fr-FR">

<head>
    <title>Dashboard Robot YOUPI</title>

    <meta charset="UTF-8">
    <link rel="stylesheet" href="Style/Style.css">
</head>

<?php include ('include/header.php') ?>

<body>
    <div id="main">
        <div class="container">

            <!-- JOINTS MOVEMENT -->
            <div class="card">
                <h2>Joints Movement</h2>
                <form action="include/move.php" method="post">

                    <label>Mode:</label>
                    <button id="mode_toggle" class="mode-toggle" type="button" onclick="toggleMode(this)">Direct</button>
                    <br><br>

                    <label for="Position_actuel">Position actuel :</label>
                    <input type="text" id="Position_actuel" name="Position_actuel" value="0" readonly>
                    <br><br>

                    <label for="Speed_joint">Speed :</label>
                    <input type="range" id="Speed_joint" name="Speed" min="0" max="100" value="0" oninput="Speed_joint_output.value = Speed_joint.value">
                    <output id="Speed_joint_output">0</output>%
                    <br><br>

                    <label for="Gripper">Gripper :</label>
                    <input type="range" id="Gripper" name="Gripper" min="0" max="100" value="0" oninput="Gripper_output.value = Gripper.value">
                    <output id="Gripper_output">0</output>%
                    <br><br>

                    <label for="Pitch">Pitch :</label>
                    <input type="range" id="Pitch" name="Pitch" min="-180" max="180" value="0" oninput="Pitch_output.value = Pitch.value">
                    <output id="Pitch_output">0</output>°
                    <br><br>

                    <label for="Roll">Roll :</label>
                    <input type="range" id="Roll" name="Roll" min="-180" max="180" value="0" oninput="Roll_output.value = Roll.value">
                    <output id="Roll_output">0</output>°
                    <br><br>

                    <label for="Elbow">Elbow :</label>
                    <input type="range" id="Elbow" name="Elbow" min="-180" max="180" value="0" oninput="Elbow_output.value = Elbow.value">
                    <output id="Elbow_output">0</output>°
                    <br><br>

                    <label for="Shoulder">Shoulder :</label>
                    <input type="range" id="Shoulder" name="Shoulder" min="-180" max="180" value="0" oninput="Shoulder_output.value = Shoulder.value">
                    <output id="Shoulder_output">0</output>°
                    <br><br>

                    <label for="Base">Base :</label>
                    <input type="range" id="Base" name="Base" min="-180" max="180" value="0" oninput="Base_output.value = Base.value">
                    <output id="Base_output">0</output>°
                    <br><br>

                    <input type="submit" value="Start Joint Movement">
                </form>
            </div>

            <!-- CARTESIAN MOVEMENT -->
            <div class="card">
                <h2>Cartesian Movement</h2>
                <form action="include/move_cartesian.php" method="post">

                    <label for="Speed_cartesian">Speed :</label>
                    <input type="range" id="Speed_cartesian" name="Speed1" min="0" max="100" value="0" oninput="Speed_cartesian_output.value = Speed_cartesian.value">
                    <output id="Speed_cartesian_output">0</output>%
                    <br><br>

                    <label for="x">X :</label>
                    <input type="number" id="x" name="x" value="0" step="0.1">
                    <br><br>

                    <label for="y">Y :</label>
                    <input type="number" id="y" name="y" value="0" step="0.1">
                    <br><br>

                    <label for="z">Z :</label>
                    <input type="number" id="z" name="z" value="0" step="0.1">
                    <br><br>

                    <label for="roll">Roll :</label>
                    <input type="number" id="roll" name="roll" value="0" step="0.1">
                    <br><br>

                    <label for="pitch">Pitch :</label>
                    <input type="number" id="pitch" name="pitch" value="-90" step="0.1">
                    <br><br>

                    <input type="submit" value="Start Cartesian Movement">
                </form>
            </div>
        </div>
    </div>

    <?php include ('include/footer.php') ?>
    <script src="js/sliders.js"></script>

    <script>
        function toggleMode(button) {
            button.textContent = (button.textContent === "Direct") ? "Commanded" : "Direct";
        }
    </script>
</body>

</html>
