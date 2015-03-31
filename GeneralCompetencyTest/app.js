$(function() {
	
	var quizModel = {
		data : [],

		init : function() {
			$.getJSON('stylesheets/quizdata.json', function(data) {
				this.data = data;
			});
		}

	};

	var octopus = {
		init : function() {
			quizModel.init();
			view.init();
		}
	};

	var testProgressView = {
		init : function() {
			// initialize the test progress view
		},

		render : function() {
			// render the test progress view
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