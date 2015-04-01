$(function() {
	
	var quizModel = {

		data : [],

		init : function(data) {
			this.data = data;
		}

		setQuizState : function(state) {
			this.quizState = state;
		},

		getQuizState : function() {
			return this.quizState;
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

		startQuiz : function() {
			// ajax call to the server side to indicate start of quiz

			// update model to reflect start of quiz
			quizModel.setQuizState("INPROGRESS");
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

		submitAnswer : function(responseAnswer, responseTS) {
			// grab the current question object from model
			// update the question object
			// with response answer and response time
			// call server side submit function
			// render question view
			// render test progress
		},

		nextQuestion : function() {
			// check if time limit exceeded
			// update the current question to the next
			// call render of question view
			// call render of test progress view
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

			// grab ui objects for question view
			this.answerButton = $("#answer");
			this.nextButton = $("#nextquestion");
			this.questionPane = $("#contentbox");
			this.startButton = $("#startbutton");

			// hide all buttons on init
			// using jquery hide function
			this.answerButton.hide();
			this.nextButton.hide();
			this.questionPane.hide();
			this.startButton.hide();

			// add event handlers
			this.answerButton.click(function(){
				// get selected answer
				var selectedAnswer;
				var responseTS = now();
				octopus.submitAnswer(selectedAnswer, responseTS);
			});

			this.nextButton.click(function() {
				octopus.nextQuestion();
			});

			this.render();
		},

		render : function() {

			// Get test status START, INPROGRESS, END
			var status = octopus.getStatus();
			var currentQuestion = octopus.getCurrentQuestion();
			
			// initialize with a start button if test not started
			if (status == "START") {
				this.startButton.show();
				return;
			}

			if (status == "INPROGRESS") {
				// display the current question
				// use template for question
				// and bind with its data
				this.answerButton.show();
				this.nextButton.show();
				return;
			}
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