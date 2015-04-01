$(function() {
	
	var quizModel = {

		data : [],

		init : function(data) {
			this.data = data;
		},

		getData : function() {
			return this.data;
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
			console.log(quizModel.getData());
			//view.init();
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