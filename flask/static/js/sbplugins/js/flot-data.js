
//Flot Moving Line Chart
$(document).ready(function() {

    var container_cpu = $("#flot-line-chart-moving-cpu");
	 var container_mem = $("#flot-line-chart-moving-mem");
	 var container_disk = $("#flot-line-chart-moving-disk");

    // Determine how many data points to keep based on the placeholder's initial size;
    // this gives us a nice high-res plot while avoiding more than one point per pixel.

    var maximum = container_cpu.outerWidth() / 2 || 300;

    //

    var data_cpu = [];
	var data_mem = [];
	var data_disk = [];
/**
data format
[[0,50],[1,56],[2,36],[3,76],.....[]]
**/
    function getRandomDataCpu() {

        if (data_cpu.length) {
            data_cpu = data_cpu.slice(1);
        }

        while (data_cpu.length < maximum) {
            var previous = data_cpu.length ? data_cpu[data_cpu.length - 1] : 50;
            var y = previous + Math.random() * 10 - 5;
            data_cpu.push(y < 0 ? 0 : y > 100 ? 100 : y);
        }

        // zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data_cpu.length; ++i) {
            res.push([i, data_cpu[i]])
        }

        return res;
    }
	function getRandomDataMem() {

        if (data_mem.length) {
            data_mem = data_mem.slice(1);
        }

        while (data_mem.length < maximum) {
            var previous = data_mem.length ? data_mem[data_mem.length - 1] : 50;
            var y = previous + Math.random() * 10 - 5;
            data_mem.push(y < 0 ? 0 : y > 100 ? 100 : y);
        }

        // zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data_mem.length; ++i) {
            res.push([i, data_mem[i]])
        }

        return res;
    }
	function getRandomDataDisk() {

        if (data_disk.length) {
            data_disk = data_disk.slice(1);
        }

        while (data_disk.length < maximum) {
            var previous = data_disk.length ? data_disk[data_disk.length - 1] : 50;
            var y = previous + Math.random() * 10 - 5;
            data_disk.push(y < 0 ? 0 : y > 100 ? 100 : y);
        }

        // zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data_disk.length; ++i) {
            res.push([i, data_disk[i]])
        }

        return res;
    }
    //

    series_cpu = [{
        data: getRandomDataCpu(),
        lines: {
            fill: true
        }
    }];
	//console.log(series_cpu[0].data);
    series_mem = [{
        data: getRandomDataMem(),
        lines: {
            fill: true
        }
    }];
	series_disk = [{
		data: getRandomDataDisk(),
		lines: {
			fill: true
		}
	}];
    //

    var plot_cpu = $.plot(container_cpu, series_cpu, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 110
        },
        legend: {
            show: true
        }
    });

    // Update the random dataset at 25FPS for a smoothly-animating chart

    setInterval(function updateRandom() {
        series_cpu[0].data = getRandomDataCpu();
        plot_cpu.setData(series_cpu);
        plot_cpu.draw();
    }, 40);
	
	
	var plot_mem = $.plot(container_mem, series_mem, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 110
        },
        legend: {
            show: true
        }
    });

	setInterval(function updateRandom() {
        series_mem[0].data = getRandomDataMem();
        plot_mem.setData(series_mem);
        plot_mem.draw();
    }, 40);
// plot disk

var plot_disk = $.plot(container_disk, series_disk, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 110
        },
        legend: {
            show: true
        }
    });

    // Update the random dataset at 25FPS for a smoothly-animating chart

    setInterval(function updateRandom() {
        series_disk[0].data = getRandomDataDisk();
        plot_disk.setData(series_disk);
        plot_disk.draw();
    }, 5000);
	
	//console.log(getRandomDataCpu());
});

