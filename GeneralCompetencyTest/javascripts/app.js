$(function() {

	var Randomiser = {
		shuffle : function (array) {
			var currentIndex = array.length, temporaryValue, randomIndex ;

			// While there remain elements to shuffle...
			while (0 !== currentIndex) {

				// Pick a remaining element...
				randomIndex = Math.floor(Math.random() * currentIndex);
				currentIndex -= 1;

				// And swap it with the current element.
				temporaryValue = array[currentIndex];
				array[currentIndex] = array[randomIndex];
				array[randomIndex] = temporaryValue;
			}

			return array;
		}
	};

	var quizModel = {

		// instance variables: title, questions

		init : function(data) {
			// create questions array from the data
			this.data = data;
			this.createQuizModel();
			console.log(this.data);
		},

		createQuizModel : function() {
			// get questions from the json and assign it to questions array
			// add section and subsection to the question object
			var questionsArray = [];
			$.each(quizModel.data, function (key, value) {

				if (key == "name")
					quizModel.title = value;

				if (key == "section") {
					$.each(value, function(index, value) {
						var sections = value;
						$.each(sections, function(key, value) {
							if (key == "subsection") {
								$.each(value, function(index, value) {
									var subsections = value;
									$.each(subsections, function(key, value) {
										if (key == "questions") {
											//if (!quizModel.questionIndex)
											//	value = Randomiser.shuffle(value);
											$.each(value, function(index, value){
												value.section = sections.name;
												value.subsections = subsections;
												value.options = Randomiser.shuffle(value.options);
												questionsArray.push(value);
											});
										}
									});
								});
							}
						});
					});
				}
			});
			this.questions = questionsArray;
			console.log(this.questions.length);
		},

		getQuizStatus : function() {
			// get the status of the quiz by looking into the questions array
			// returns START, INPROGRESS, END
			var q, qStatus;
			$.each(this.questions, function(index, value) {
				q = index;
				qStatus = value.status;
				if(!value.status)
					return false;
			});

			this.questionIndex = q;

			if (q == 0)
				return "START";
			else if (q == this.questions.length - 1 && qStatus)
				return "END";
			else
				return "INPROGRESS";
		},

		nextQuestion : function() {
			// returns the next questions and updates the pointer
			var quizStatus = this.getQuizStatus();
			console.log(quizStatus);
			if (quizStatus == "START")
				this.questionIndex = 0;
			if (quizStatus == "END"){
				this.questionIndex = this.questions.length;
				this.question = undefined;
			}

			if (this.questionIndex < this.questions.length)
				this.question = this.questions[this.questionIndex++];

		},

		setQuestion : function(index) {
			$.each(this.questions, function(i, q){
				if (i < index)
					q.status = "skip";
			});
			this.questionIndex = index - 1;
			this.question = this.questions[this.questionIndex];
		}
	};

	var octopus = {

		init : function() {
			startView.init();

			$.ajax({
				url: "/getquizstatus",
				dataType: 'json',
				async: false,
				success: function(data) {
					quizModel.init(data);
				}
			});

			var status = quizModel.getQuizStatus();
			if (status == "END")
				resultView.init();
			else
				startView.render();			
		},

		submitAnswer : function() {
			var submittedQuestion = $.extend({},quizModel.question);
			if(quizModel.question.type == 'essay')
				questionView.stopautosave();
			
			submittedQuestion.subsections = undefined;
			data = JSON.stringify(submittedQuestion);
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
						console.log(data);
						console.log(xhr.status);
						console.log(thrownError);
					}
				}
			});
		},

		autosaveContent : function(responseAnswer, responseTS) {
			// grab the current question object from model
			var q = quizModel.question;

			// update the question object
			// with response answer and response time
			q.responseAnswer = responseAnswer;
			q.responseTime = responseTS;
			console.log(q);
			// call server side submit function
            // creating json file for submit response
                var data = {"currentQuestion": q.id, "draft":responseAnswer,"responsetime":q.responseTime}
                data=JSON.stringify(data);
                console.log(data);
                $.ajax({
							   url: "/autosaveEssay",
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

        },        

		getResults : function() {
			$.ajax({
				type: 'get',
				url: '/getResult',
				dataType:'json',
				async: false,
				success: function (data) {
					data = JSON.stringify(data);
					quizModel.result = JSON.parse(data);
				},
				error: function () {
					alert("failure");
				}
			});
		}

	};

	var startView = {
		init : function() {
			this.titlePane = $(".title");
			this.sectionName = $("#section-name");
			this.questionPane = $("#content-box");
			
			this.startMessage = "Click the Start Test button to begin.";
			this.resumeMessage = "You have started the test, click the button below to resume the test.";
			this.resumeMessage += " Click the Resume Test button to resume.";

			this.navBar = $("#nav-bar");
			this.startButton = $("#start-btn");
			this.answerButton = $("#answer");
			this.nextButton = $("#nextquestion");
			this.startButton.hide();
			this.answerButton.hide();
			this.nextButton.hide();

			this.startButton.click(function(){
				startView.startButton.hide();
				quizModel.nextQuestion();
				questionView.init();
				questionView.render();
				progressView.init();
			});
		},

		render : function() {
			this.titlePane.html(quizModel.title);
			var quizStatus = quizModel.getQuizStatus();
			if(quizStatus == "START") {
				this.questionPane.html('<h3>' + this.startMessage + '</h3><br>');
			} else if (quizStatus == "INPROGRESS") {
				this.questionPane.html(this.resumeMessage);
				this.startButton.html("Resume Test");
			}
			this.startButton.show();
		}
	};

	var questionView = {
		init : function() {
			// get references to all html elements
			this.titlePane = $(".title");
			this.sectionName = $("#section-name");
			this.questionPane = $("#content-box");
			this.questionNote = $("#question-instructions");

			this.navBar = $("#nav-bar");
			this.startButton = $("#start-btn");
			this.answerButton = $("#answer");
			this.nextButton = $("#nextquestion");

			this.answerButton.click(function(){

				var q = quizModel.question;
				var selectedAnswer = $("input:checked").val();

				if (q.subsections.types == "essay") {
					selectedAnswer = $("textarea").val();
					if (!selectedAnswer)
						selectedAnswer = "skip";
				}

				if (q.subsections.types == "record") {
					// make a call to a separate handler
					selectedAnswer = "submitted";
				}

				if (selectedAnswer == "skip") {
					q.status = "skip";
					q.responseAnswer = "skip";
					questionView.submittedTS = Date.now();
					q.responseTime = questionView.getResponseTime();
					octopus.submitAnswer();
					questionView.nextButton.show();
				} else if (selectedAnswer){
					q.status = "submitted";
					q.responseAnswer = selectedAnswer;
					questionView.submittedTS = Date.now();
					q.responseTime = questionView.getResponseTime();
					octopus.submitAnswer();
					questionView.nextButton.show();
				} else {
					alert("Select a choice to submit answer.");
				}
				progressView.init();
			});

			this.nextButton.click(function(){
				questionView.nextButton.hide();
				quizModel.nextQuestion();
				console.log(quizModel.question, quizModel.questionIndex);
				if(quizModel.question){
					questionView.render();
					progressView.init();
				}
				else
					resultView.init();
			});
		},

		render : function() {
			var q = quizModel.question;
			this.sectionName.html("<h4>");
			this.sectionName.append(q.section + "&nbsp; - &nbsp;");
			this.sectionName.append(q.subsections.name);
			this.sectionName.append("</h4>");
			this.questionNote.html('<p class="lead">' + q.subsections.note + '</p>');
			this.questionPane.html('<p class="lead">' + q.question + '</p>');
			
			if (q.subsections.types == "passage"){
				this.displayPassage();
				this.displayOptions();
			}

			if (q.subsections.types == "essay")
			{
				this.displayEssay();
				this.myvar = setInterval(function() {    					
    							var text = $('textarea').val();    					
    							octopus.autosaveContent(text,Date.now()/(1000*60));
    						},30000);

				// $("textarea").on('input propertychange',function() {
				//  			console.log('Textarea Change');
				// 			setTimeout(function() {    					
    // 							var text = $('textarea').val();    					
    // 							octopus.autosaveContent(text,Date.now()/(1000*60));
    // 						},30000);
				// 		});
			}	
			if (q.subsections.types == "video"){
				this.displayVideo();
				this.displayOptions();
			}
			if (q.subsections.types == "record")
				this.displayRecording();
			if (q.subsections.types == "question")
				this.displayOptions();
			this.appearedTS = Date.now();
			this.answerButton.show();
		},

		stopautosave : function(myvar) {
			clearInterval(myVar);
		},

		displayQuestion : function(q) {
			var optionsHTML = '<div>' + q.question + '</div>';
			for (var i = 0; i < q.options.length; i++) {
				var optionText = q.options[i].substring(1, q.options[i].length);
				optionsHTML += '<div class="radio">';
				optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="' + optionText + '"';
				if(q.status && q.responseAnswer == optionText)
					optionsHTML += 'checked';
				optionsHTML += '>' + optionText + '</label>';
				optionsHTML += '</div>';
			}
			optionsHTML += '<div class="radio">';
				optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="skip">Skip Question</label>';
				optionsHTML += '</div>';
			return optionsHTML;
		},

		displayPassage : function() {
			var q = quizModel.question;
			this.questionNote.append('<div>' + q.subsections.passage +'</div>');
		},

		displayEssay : function() {
			var q = quizModel.question;
			this.questionNote.html("");
			this.questionPane.append('<div><textarea style="width: 600px; height: 200px"></textarea>');
		},

		displayVideo : function() {
			var q = quizModel.question;
			this.questionNote.append(q.subsections.link);
		},

		displayRecording : function() {
			var q = quizModel.question;
			this.questionPane.append('<div><button id="record" class="btn btn-danger">Record</button>' + 
				'&nbsp;&nbsp<button id="stop" class="btn btn-info">Stop</button></div>');
				var record=document.getElementById('record');
				var stop=document.getElementById('stop');
				record.onclick= function(){
					alert("There is a notification on the top of the browser seeking your permission to record audio. Click Ok and then Allow recording to begin.");
					record.disabled=true;
					stop.disabled=false;
					interfaceRecord();
				}
				stop.onclick= function() {
					$("#record").hide();
					$("#stop").hide();
					record.disabled=false;
					stop.disabled=true;
					interfaceStop();
				}
				window.onbeforeunload = function() {
                if (!!fileName) {
                deleteAudioVideoFiles();
                return 'It seems that you\'ve not deleted audio/video files from the server.';
            }
        };
		},

		displayOptions : function() {
			var q = quizModel.question;
			var optionsHTML = '';
			for (var i = 0; i < q.options.length; i++) {
				var optionText = q.options[i].substring(1, q.options[i].length);
				optionsHTML += '<div class="radio">';
				optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="' + optionText + '"';
				if(q.status && q.responseAnswer == optionText)
					optionsHTML += 'checked';
				optionsHTML += '>' + optionText + '</label>';
				optionsHTML += '</div>';
			}
			optionsHTML += '<div class="radio">';
			optionsHTML += '<label><input type="radio" name="optionsRadios" id="optionsRadios1" value="skip">Skip Question</label>';
			optionsHTML += '</div>';
			this.questionPane.append(optionsHTML);
		},

		getResponseTime : function() {
			return (questionView.submittedTS - questionView.appearedTS)/(100 * 60);
		}
	};

	var progressView = {

		init : function() {
			// get references to all html elements
			this.progressBox = $("#progress-box");
			this.progressBox.html("");
			this.render();
		},

		render : function() {
			progressView.progressBox.append('<h3>Test Progress</h3><div style="display: flex">');
			var section, buttonCount = 0;
			$.each(quizModel.questions, function(index, question){

				if(section != question.section){
					buttonCount = 0;
					if(section){
						progressView.progressBox.append("</div></div>");
					}
					section = question.section;
					var sectionLabel = '<div style="display: flex"><div><b>' +
										 section + '</b></div><div>';
					progressView.progressBox.append(sectionLabel);
				}
				if(index < 8)
					buttonLabel = '&nbsp;' + (index + 1);
				else
					buttonLabel = index + 1;

				if(!question.status)
					buttonColor = "btn-default";
				if(question.status == "skip")
					buttonColor = "btn-warning";
				if(question.status == "submitted")
					buttonColor = "btn-success";
				if(question == quizModel.question)
					buttonColor = "btn-primary";

				qButtonHTML = '<button class="btn btn-xs ' + buttonColor + '" id="qbutton' + index + '">' + buttonLabel + '</button>&nbsp;';
				buttonCount++;

				progressView.progressBox.append(qButtonHTML);
			});
		},

		reset : function() {
			this.progressBox.html("");
		}
	};

	var resultView = {
		init : function() {
			// get references to all html elements
			this.titlePane = $(".title");
			this.sectionName = $("#section-name");
			this.questionPane = $("#content-box");
			this.questionNote = $("#question-instructions");

			this.navBar = $("#nav-bar");
			this.startButton = $("#start-btn");
			this.answerButton = $("#answer");
			this.nextButton = $("#nextquestion");
			
			this.startButton.hide();
			this.answerButton.hide();
			this.nextButton.hide();

			this.render();
		},

		render : function() {
			progressView.init();
			progressView.reset();
			this.sectionName.html("You have completed the test and the following is your test report.");
			octopus.getResults();
			var resultHTML = '<table class="table table-hover">';
			resultHTML += '<tr><th>Q. No.</th><th>Score</th><th>Response Time</th></tr>';
			totalScore = 0;
			$.each(quizModel.result.question,function(index, value){
				//console.log(value.currentQuestion, value.q_score, value.responsetime);
				resultHTML += '<tr><td>' + value.currentQuestion + '</td>';
				resultHTML += '<td>' + value.q_score + '</td>'
				resultHTML += '<td>' + Math.round(value.responsetime) + '</td></tr>';
				totalScore += value.q_score;
			});
			resultHTML += '</table>';
			this.questionNote.html('<p class="lead">Your total score is: ' + totalScore + '</p>');
			this.questionPane.html(resultHTML);
		}
	};

	octopus.init();
});