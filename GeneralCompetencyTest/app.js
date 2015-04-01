$(function() {
	
	var quizModel = {

		data : [],

		init : function(data) {
			this.data = data;
		}
	};

	var octopus = {
		init : function() {
			$.ajax({
				url: "quizdata.json",
				dataType: 'json',
				async: false,
				success: function(data) {
					quizModel.init(data);	
				}
			});

			testProgressView.init();
			questionView.init();
			testResultView.init();
		},

		getQuizTitle : function() {
			return quizModel.data.name;
		},

		getQuizSubsection : function() {
			var currentSection = 0;
			var currentSubsection = 0;
			return quizModel.data.section[currentSection].name + ' - ' + quizModel.data.section[currentSection].subsection[currentSubsection].name;
		},

		ProgressButtonsBar : function() {
			for (var i=1; i<=30; i++){
				$("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-default btn-xs">'+i+'</button>&nbsp;');
				$("#"+i).addClass('disabled');
			}
		},
		initStartButton : function() {
			$("#contentbox").html(
				"<button id='starttest' class='btn btn-success'>Click to Start Test</button>"
			);
		}
	};

	var testProgressView = {

		title : $(".title"),
		subsection : $("#h4"),

		init : function() {
			// initialize the test progress view
			this.render();
		},

		render : function() {
			// render the test progress view
			this.title.html(octopus.getQuizTitle());
			this.subsection.html(octopus.getQuizSubsection());
			octopus.ProgressButtonsBar();
		}
	};

	var questionView = {
			
		init : function() {
			this.render();
		},

		render : function() {
			// initialize with a start button
				octopus.initStartButton();
			// initialize the submit answer button

			// initialize the continue button

			// dispaly the question using the question type and data template approach
		}
	};

	var testResultView = {

		init : function() {

		},

		render : function() {

		}

	};

	octopus.init();
});