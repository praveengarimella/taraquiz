$(function() {
	
	var quizModel = {
		init : function(data) {
			this.data = data;
			this.quizState = "START";

			this.questionIndex = 0;
			this.subSectionIndex = 0;
			this.sectionIndex = 0;

			this.currentSection = data.section[this.sectionIndex];
			this.sections = data.section;

			this.currentSubsection = this.currentSection.subsection[this.subSectionIndex];
			this.subsections = this.currentSection.subsection;

			this.questions = this.currentSection.subsection[0].questions;
		},

		nextSubsection : function() {
			if (this.subSectionIndex < this.subsections.length - 1) {
				this.subSectionIndex++;
				this.currentSubsection = this.subsections[this.subSectionIndex];
				this.questionIndex = 0;
				this.questions = this.currentSubsection.questions;
			} else if (this.subSectionIndex == this.subsections.length - 1) {
				this.nextSection();
			}
		},

		nextSection : function() {
			if (this.sectionIndex < this.sections.length - 1) {
				this.sectionIndex++;
				this.currentSection = this.sections[this.sectionIndex];
				this.subsections = this.currentSection.subsection;
				this.subSectionIndex = 0;
				this.currentSubsection = this.subsections[this.subSectionIndex];
				this.questions = this.currentSubsection.questions;
				this.questionIndex = 0;
			} else if (this.sectionIndex == this.sections.length - 1)
				this.quizState = "END";
		}
	};

	var octopus = {
		
		init : function() {

			// load json and assign to quiz model
			// note: ajax call is sync
			$.ajax({
				url: "stylesheets/quizdata.json",
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
			quizModel.quizState = "INPROGRESS";
			questionView.render();
		},

		getQuizTitle : function() {
			return quizModel.data.name;
		},

		getQuizSubsection : function() {
			return quizModel.currentSection.name + ' - ' 
					+ quizModel.currentSubsection.name;
		},

		// todo fix MVC pattern issue
		ProgressButtonsBar : function() {
			for (var i=1; i<=30; i++){
				$("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-default btn-xs">'+i+'</button>&nbsp;');
				$("#"+i).addClass('disabled');
			}
		},

		submitAnswer : function(responseAnswer, appearedTS, responseTS) {
			// grab the current question object from model
			var q = this.getCurrentQuestion();

			// update the question object
			// with response answer and response time
			q.responseAnswer = responseAnswer;
			q.responseTime = (responseTS - appearedTS) / (1000 * 60);
			// call server side submit function
            // creating json file for submit response
                var data = {"currentQuestion": q.id, "submittedans":responseAnswer,"responsetime":q.responseTime}
                data=JSON.stringify(data);
                $.ajax({
							   url: "/submitanswer",
							   type: 'GET',
							   contentType:'application/json',
							   data: {
									jsonData: data
								},
							   dataType:'json',
							   success: function(data){
								 //On ajax success do this
								 console.log(data);
								  },
							   error: function(xhr, ajaxOptions, thrownError) {
								  //On error do this
									if (xhr.status == 200) {

										 console.log(ajaxOptions);
									}
									else {
										console.log(xhr.status);
										console.log(thrownError);
									}
								}
			 });
			// render question view
			// render test progress
		},

		getStatus : function() {
			return quizModel.quizState;
		},

		getCurrentQuestion : function() {
			return quizModel.questions[quizModel.questionIndex];
		},

		getCurrentSubsection : function() {
			return quizModel.subsections[quizModel.subSectionIndex];
		},

		nextQuestion : function() {
			
			if (quizModel.questionIndex <= quizModel.questions.length)
				quizModel.questionIndex++;

			if (quizModel.questionIndex == quizModel.questions.length) {
				quizModel.nextSubsection();
			}

			questionView.render();
		}
	};

	var testProgressView = {

		init : function() {
			this.pageTitle = $(".title");
			this.subSection = $("#h4");
			this.render();
		},

		render : function() {
			// render the test progress view
			this.pageTitle.html(octopus.getQuizTitle());
			this.subSection.html(octopus.getQuizSubsection());
			
			// todo fix the MVC pattern issue
			//var testProgress = octopus.getTestProgress();
			
		}
	};

	var questionView = {
			
		init : function() {

			// grab ui objects for question view
			this.answerButton = $("#answer");
			this.nextButton = $("#nextquestion");
			this.questionPane = $("#contentbox");
			this.startButton = $("#startbutton");
			this.typeBox = $("#typeBox");

			// hide all buttons on init
			// using jquery hide function
			this.answerButton.hide();
			this.nextButton.hide();
			//this.questionPane.hide();
			this.startButton.hide();

			// add event handlers
			this.answerButton.click(function(){
				// get selected answer
				var selectedAnswer = $("input:checked").val();
				var subsection = octopus.getCurrentSubsection();
				if (subsection.types == "essay")
						selectedAnswer = $("textarea").val();
				var responseTS = Date.now();
				octopus.submitAnswer(selectedAnswer, questionView.appearedTS, responseTS);
				questionView.nextButton.show();

				testProgressView.render();
			});

			this.nextButton.click(function() {
				octopus.nextQuestion();
				testProgressView.render();
			});

			this.startButton.click(function() {
				octopus.startQuiz();
			});

			this.render();
		},

		render : function() {

			// Get test status START, INPROGRESS, END
			var status = octopus.getStatus();
			
			
			// initialize with a start button if test not started
			if (status == "START") {
				this.startButton.show();
			}

			if (status == "INPROGRESS") {
				
				var currentQuestion = octopus.getCurrentQuestion();
				var subsection = octopus.getCurrentSubsection();
				if (currentQuestion) {
					this.questionPane.html(this.displayQuestion(currentQuestion));
					if (subsection.types == "passage")
						this.displayPassage();
					if (subsection.types == "essay")
						this.displayEssay();
					if (subsection.types == "video")
						this.displayVideo();
					if (subsection.types == "record")
						this.displayRecording();
					if (subsection.types == "question")
						this.displayQuestionNote();
					// get the appeared timestamp for response time calc
					this.appearedTS = Date.now();
				}
				// display the current question
				// use template for question
				// and bind with its data
				this.startButton.hide();
				this.answerButton.show();
				this.nextButton.hide();
			}

			if (status == "END") {
				this.answerButton.hide();
				this.nextButton.hide();
				testResultView.render();
			}
		},

		displayQuestion : function(path) {
			var optionsHTML = '<div id="typeBox"></div><br><div>' + path.question + '</div>';
			for (var i = 0; i < path.options.length; i++) {
				var optionText = path.options[i].substring(1, path.options[i].length);
				optionsHTML += '<div class="radio">';
				optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="' + optionText + '">' + optionText + '</label>';
				optionsHTML += '</div>';
			}
			optionsHTML += '<div class="radio">';
				optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="skip">Skip Question</label>';
				optionsHTML += '</div>';
			return optionsHTML;
		},

		displayPassage : function() {
			var subsection = octopus.getCurrentSubsection();
			$("#typeBox").html('<h4>' + subsection.note + '</h4><div>' + 
					subsection.passage+'</div>');
		},

		displayEssay : function() {
			var subsection = octopus.getCurrentSubsection();
			$("#typeBox").html('<h4>' + subsection.note + 
				'</h4><textarea style="width: 600px; height: 200px">');
		},

		displayVideo : function() {
			var subsection = octopus.getCurrentSubsection();
			$("#typeBox").html("<h4>" + subsection.note + 
				"</h4>" + subsection.link);
			console.log(subsection.link);
		},

		displayRecording : function() {
			var subsection = octopus.getCurrentSubsection();
				$("#contentbox").append('<button class="btn btn-danger">Record</button>&nbsp;&nbsp<button class="btn btn-info">Stop</button>');
		},

		displayQuestionNote : function() {
			var subsection = octopus.getCurrentSubsection();
				$("#typeBox").html('<div><b>' + subsection.note + '</b></div>');
		}
	};

	var testResultView = {

		init : function() {
			this.contentbox = $("#contentbox");
		},

		render : function() {
			this.contentbox.html("End of the test!");
			document.getElementById("result").style.display="block";

		}

	};

	octopus.init();
});
