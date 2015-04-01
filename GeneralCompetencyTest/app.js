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
		}
	};

	var testProgressView = {

		title : $(".title"),

		init : function() {
			// initialize the test progress view
			this.render();
		},

		render : function() {
			// render the test progress view
			console.log("inside render" + octopus.getQuizTitle());
			this.title.html(octopus.getQuizTitle());
		}
	};

	var questionView = {
		init : function() {
			// initialize with a start button

			// initialize the submit answer button

			// initialize the continue button
		},

		render : function() {
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