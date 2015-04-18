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
			this.data = data
			// create questions array from the data
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
				if (key == "testEnd")
					quizModel.testEnd = value;

				if (key == "section") {
					$.each(value, function(index, value) {
						var sections = value;
						$.each(sections, function(key, value) {
							if (key == "subsection") {
								$.each(value, function(index, value) {
									var subsections = value;
									$.each(subsections, function(key, value) {
										if (key == "questions") {
											function compare(a,b) {
												if (a.serialno < b.serialno)
													return -1;
												if (a.serialno > b.serialno)
													return 1;
												return 0;
											}
											value.sort(compare);
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
			else if (quizModel.testEnd || q == this.questions.length - 1 && qStatus)
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
			//$.each(this.questions, function(i, q){
			//	if (i < index)
			//		q.status = "skip";
			//});
			this.questionIndex = index;
			this.question = this.questions[this.questionIndex];
		}
	};
	var octopus = {
		init : function() {
			$.post("/getquizstatus")
				.done(function(data){
					console.log("info: questions loaded from server");
					data = JSON.parse(data);
					quizModel.init(data)
					startView.init();
					var status = quizModel.getQuizStatus();
					console.log("quiz status" + status);
					if (status == "END")
						resultView.init();
					else
						startView.render();
				})
				.fail(function(data){
					startView.init();
					startView.showError();
				});
		},
		startTest : function() {
			octopus.pingServer();
			this.pingThread = window.setInterval(function(){
				octopus.pingServer();
			}, 60000);
		},
		submitAnswer : function() {
			var submittedQuestion = $.extend({},quizModel.question);

			if(quizModel.question.subsections.types == 'essay')
				questionView.stopautosave();

			submittedQuestion.subsections = undefined;
			data = JSON.stringify({jsonData: submittedQuestion});
			$.post("/submitanswer", data)
				.done(function(data){
					console.log("Success:" + data);
					data = JSON.parse(data)
					if(data.testEnd)
						quizModel.testEnd = true;
					if(quizModel.getQuizStatus() == "END")
						resultView.init();
					if(quizModel.getQuizStatus() == "INPROGRESS")
						questionView.showNextQuestion();
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
			data=JSON.stringify({jsonData: data});
			$.post("/autosaveEssay", data)
				.done(function(data){
					console.log("Success:" + data);
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
		},
		pingServer : function() {
			$.post("/testtime")

				.done(function(data){
					console.log("ping response " + data)
					data = JSON.parse(data);
					console.log(data.timeRemaining);
					if(!data.timeRemaining) {
						this.pingThread = clearInterval();

					}
					progressView.renderTime(data.timeRemaining);
				})
				.fail(function(){
					console.log("PING Failed");
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
			this.errorMessage = "There is a problem with starting your test session. Refresh the page. ";
			this.errorMessage += "If the problem persists then report Error 100 to your test administrator.";

			this.navBar = $("#nav-bar");
			//add this button in JS
			//<button id="start-btn" class="btn btn-lg btn-success">Start Test</button>
			// create start/resume button
			var btn = document.createElement("BUTTON");
			var t = document.createTextNode("Start Test");
			btn.appendChild(t);
			btn.setAttribute("id", "start-btn");
			this.navBar.append(btn);

			this.startButton = $("#start-btn");
			this.answerButton = $("#answer");
			this.startButton.hide();
			this.answerButton.hide();
            
            var btn2 = document.createElement("BUTTON");
    		var t2 = document.createTextNode("Start Test");
    		btn2.appendChild(t2);
			btn2.setAttribute("id", "start");
    		this.navBar.append(btn2);
			this.startButton = $("#start");
			this.startButton.addClass("btn btn-success")

			this.startButton.click(function(){
				startView.startButton.hide();
				if(quizModel.testEnd)
					resultView.init();
				else {
					octopus.startTest();
					quizModel.nextQuestion();
					questionView.init();
					questionView.render();
					progressView.init();
				}
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
				this.startButton.addClass("btn btn-info");
			}
			this.startButton.show();
		},

		showError : function() {
			this.questionPane.html('<p class="lead">' + this.errorMessage + '</p>');
			this.startButton.hide();
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

			// create answer button
			var btn = document.createElement("BUTTON");
			var t = document.createTextNode("Submit Answer");
			btn.appendChild(t);
			btn.setAttribute("id", "sanswer");
			this.navBar.append(btn);
			this.answerButton = $("#sanswer");
			this.answerButton.addClass("btn btn-success")

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
				} else if (selectedAnswer){
					q.status = "submitted";
					q.responseAnswer = selectedAnswer;
					questionView.submittedTS = Date.now();
					q.responseTime = questionView.getResponseTime();
					octopus.submitAnswer();
				} else {
					alert("Select a choice to submit answer.");
				}
				progressView.init();
			});
		},

		showQuestion : function(){
			console.log(quizModel.question);
			if(quizModel.question){
				questionView.render();
				progressView.init();
			}
			else
				resultView.init();
		},

		showNextQuestion: function() {
			quizModel.nextQuestion();
			console.log(quizModel.question, quizModel.questionIndex);
			if(quizModel.question){
				questionView.render();
				progressView.init();
			}
			else
				resultView.init();

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

		stopautosave : function() {
			clearInterval(this.myvar);
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
			var essayText = "";
			if(quizModel.question.responseAnswer)
				essayText = quizModel.question.responseAnswer;
			this.questionPane.append('<div><textarea style="width: 600px; height: 200px">' +
			essayText + '</textarea>');
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
		},

		reset : function() {
			this.questionPane.hide();
			this.navBar.hide();
		}
	};

	var progressView = {

		init : function() {
			// get references to all html elements
			this.progressBox = $("#progress-box");
			this.progressBox.html("");
			this.timeBox = $("#time-box");
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
					buttonLabel = ' ' + (index + 1);
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

				var btn = document.createElement("BUTTON");
				var t = document.createTextNode(buttonLabel + ' ');
				btn.appendChild(t);
				btn.setAttribute("id", index);

				//qButtonHTML = '<button class="btn btn-xs ' + buttonColor + '" id="qbutton' + index + '">' + buttonLabel + '</button>&nbsp;';
				buttonCount++;

				progressView.progressBox.append(btn);
				$("#"+index).addClass("btn btn-xs " + buttonColor);
				if(!question.status)
					$("#"+index).attr('disabled','disabled');
				$("#"+index).click(function(){
					quizModel.setQuestion(this.id);
					questionView.showQuestion();
				});
			});
		},

		reset : function() {
			this.progressBox.html("");
		},

		renderTime : function(remainingTime) {
			if(!remainingTime)
				remainingTime = 0;
			buttonColor = "btn-primary";
			remainingTime = Math.round(remainingTime/60);
			buttonText = remainingTime + " minutes remaining";
			if(remainingTime <= 5) {
				buttonColor = "btn-warning";
			}
			if(remainingTime == 1) {
				buttonColor = "btn-danger";
				buttonText = "One minute left..."
			}
			if(remainingTime <= 0) {
				buttonColor = "btn-danger";
				buttonText = "Time is up!"
				window.setInterval(function(){
					location.reload();
				},3000);
				resultView.init();
			}
			this.timeBox.html('<button type="button" class="btn btn-lg btn-block '+ buttonColor +'">'+
			buttonText +'</button>');

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

			this.startButton.hide();
			this.answerButton.hide();

			this.render();
		},

		render : function() {
			progressView.init();
			progressView.reset();
			this.sectionName.html("You have completed the test.");
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
			this.questionPane.hide();
			this.navBar.hide();
		}
	};

	octopus.init();
});