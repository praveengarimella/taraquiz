window.setInterval(function(){myTimer()},4000);
function myTimer() {
	 var objectData =
         {
             timesec: 4000,
             emailid:"s@g.c" 
         };

        var objectDataString = JSON.stringify(objectData);
        console.log(objectDataString);
        $.ajax({
            type: 'get',
            url: '/testtime',
            dataType: 'json',
            data: {
                jsonData: objectDataString
            },
            success: function (data) {
                f=true;
				console.log(JSON.stringify(data));
               // alert( JSON.stringify(data));

            },
            error: function () {
                alert("failure");
            }
        });
}




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
				url: "quizdata.json",
				dataType: 'json',
				async: false,
				success: function(data) {
					quizModel.init(data);
				}
			});

			//testProgressView.init();
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
			var currentSection = 0;
			var currentSubsection = 0;
			return quizModel.data.section[currentSection].name + ' - ' + quizModel.data.section[currentSection].subsection[currentSubsection].name;
		},

		// todo fix MVC pattern issue
		ProgressButtonsBar : function() {
			for (var i=1; i<=30; i++){
				$("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-default btn-xs">'+i+'</button>&nbsp;');
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
			console.log(q);
			// call server side submit function
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
			this.pageTitle = $(".title"),
			this.subSection = $("#h4"),
			// initialize the test progress view
			this.render();
		},

		render : function() {
			// render the test progress view
			this.pageTitle.html(octopus.getQuizTitle());
			this.subSection.html(octopus.getQuizSubsection());
			
			// todo fix the MVC pattern issue
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
				var responseTS = Date.now();
				octopus.submitAnswer(selectedAnswer, questionView.appearedTS, responseTS);
				questionView.nextButton.show();
			});

			this.nextButton.click(function() {
				octopus.nextQuestion();
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
			$("#typeBox").html('<h4>' + subsection.note + 
				'</h4><iframe width="560" height="315" src="' + subsection.link +
				 '" frameborder="0" allowfullscreen></iframe>');
		}

		// function displayRecording() {
		// 	if(quizdata.section[currentSection].subsection[currentSubsection].types == "record"){
		// 		$("#typeBox").html('<h4>'+quizdata.section[currentSection].subsection[currentSubsection].note+'</h4><div></div>');
		// 	}
		// }
	};

	var testResultView = {

		init : function() {
			this.contentbox = $("#contentbox");
		},

		render : function() {
			this.contentbox.html("End of the test!");
		}

	};

	octopus.init();
});