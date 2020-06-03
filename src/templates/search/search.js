
(function () {
    var countries = null;
    var students = null;
    function loadTimeline() {
        var xmlhttp = new XMLHttpRequest();
        var dirs = location.href.split("/");
        var pardir = "";
        for (var i = 0; i < dirs.length - 1; i++)
            pardir += dirs[i] + "/";
        xmlhttp.open("GET", pardir + "timeline.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function () {
            // Let's ignore xmlhttp.status as it doesn't work local
            if (xmlhttp.readyState == 4 && xmlhttp.responseText != null) {
                contests = new Map();
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    var ps = lines[i].split(",");
                    if (ps.length >= 3) {
                        contests.set(ps[2], ps[2] + " " + ps[1]);
                    }
                }
            }
        }
        xmlhttp.send();
    }
    function loadStudents() {
        var xmlhttp = new XMLHttpRequest();
        var dirs = location.href.split("/");
        var pardir = "";
        for (var i = 0; i < dirs.length - 1; i++)
            pardir += dirs[i] + "/";
        xmlhttp.open("GET", pardir + "students.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function () {
            // Let's ignore xmlhttp.status as it doesn't work local
            if (xmlhttp.readyState == 4 && xmlhttp.responseText != null) {
                students = [];
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    var ps = lines[i].trim().split(",");
                    if (ps.length >= 9 && ps[8] === "False") {
                        students.push({
                            rawData: lines[i].trim(),
                            month: ps[0],
                            userId: ps[1],
                            name: ps[2],
                            scores: ps[3].split("-"),
                            totalScore: ps[4],
                            rank: ps[5],
                            contestName: ps[6],
                            medal: ps[7]
                        });
                    }
                }
            }
        }
        xmlhttp.send();
    }
    window.mods_search = function () {
        if (!students) return;
        if (!contests) contests = new Map();
        var html = "";
        var t_row = document.getElementById("t_row").innerHTML;
        var t_gold = document.getElementById("t_gold").innerHTML;
        var t_silver = document.getElementById("t_silver").innerHTML;
        var t_bronze = document.getElementById("t_bronze").innerHTML;
        var t_honourable = document.getElementById("t_honourable").innerHTML;
        var query = document.getElementById("search_query").value;
        query = asciify(query).toLowerCase().trim();
        if (query.length == 0) return;
        for (var i = 0; i < students.length; i++) {
            if (students[i].rawData.indexOf(query) == -1) {
                continue;
            }
            var row = t_row.replace(/{{userId}}/g, students[i].userId)
                .replace(/{{name}}/g, students[i].name)
                .replace(/{{month}}/g, students[i].month)
                .replace(/{{contest}}/g, contests.get(students[i].month) || "")
                .replace(/{{totalScore}}/g, students[i].totalScore)
                .replace(/{{rank}}/g, students[i].rank)
            switch (students[i].medal) {
                case "G":
                    row = row.replace(/{{medal}}/g, t_gold);
                    break;
                case "S":
                    row = row.replace(/{{medal}}/g, t_silver);
                    break;
                case "B":
                    row = row.replace(/{{medal}}/g, t_bronze);
                    break;
                case "H":
                    row = row.replace(/{{medal}}/g, t_honourable);
                    break;
                default:
                    row = row.replace(/{{medal}}/g, "");
                    break;
            }
            html += "<tr>" + row + "</tr>";
        }
        document.getElementById("search_results").innerHTML = html;
    }
    loadTimeline();
    loadStudents();
})();
