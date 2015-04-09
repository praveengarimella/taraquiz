$(function() {
	
	var quizModel = {
		init : function(data) {
			this.data = data;
			this.id=this.checkquizstatus(data);
            console.log(this.quizState);
			this.quizState = "START";
        
			this.questionIndex = this.id;
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
		},

        checkquizstatus: function(data) {
        	this.data=data;
            this.subsection = data.section[0].subsection;
            for(var i=0;i<this.subsection.length;i++)
            	{
            		for(var j=0;j<this.subsection[i].questions.length;j++)
            		{
            			this.questions=this.subsection[i].questions;
            			for(var k=0;k<this.questions.length;k++)
            			{
            				this.question=this.questions[k];
            				console.log("qstatus-"+this.question.status+" k-"+k);
            				if(!this.question.status)
            				{
            					console.log("qid"+this.question.id-1);
            			     return this.question.id-1;
                                  
                            }
            			}
            		}
            	}
        }
	};

	var octopus = {
		
		init : function() {

			// load json and assign to quiz model
			// note: ajax call is sync
			$.ajax({
				url: "/getquizstatus",
				dataType: 'json',
				async: false,
				success: function(data) {
					quizModel.init(data);
				}
			});

			testProgressView.init();
			questionView.init();
			testResultView.init();
			//octopus.ProgressButtonsBar();
		},

		startQuiz : function() {
			// ajax call to the server side to indicate start of quiz
				
			// update model to reflect start of quiz
			quizModel.quizState = "INPROGRESS";
			testProgressView.render();
			questionView.render();
			
		},

		getQuizTitle : function() {
			return quizModel.data.name;
		},

		getQuizSubsection : function() {
			return quizModel.data.section[quizModel.sectionIndex].name+ ' - ' 
			      + quizModel.data.section[quizModel.sectionIndex].subsection[quizModel.subSectionIndex].name;
		},

		getProgress : function()
	    {
	    	var i=1;
	    	this.questionArray=[]
	    	for( var sindex=0;sindex<quizModel.data.section.length;sindex++)
	    	{
               for(var ssindex=0;ssindex<quizModel.data.section[sindex].subsection.length;ssindex++)
               {
                    for(var qindex=0;qindex<quizModel.data.section[sindex].subsection[ssindex].questions.length;qindex++)
                    {
                    	this.questionArray[i]=quizModel.data.section[sindex].subsection[ssindex].questions[qindex];
                    	i++;
               		}       

                }
	    	}

	    	return this.questionArray;
	    },

	    getQuestions : function() {
	    	var questionsArray = [];
	    	var subSectionIndex, sectionIndex;
	    	$.each(quizModel.data, function (key, value) {
	    		if (key == "section") {
	    			sections = value;
	    			$.each(sections, function(index, value){
	    				sectionIndex = index;
	    				var subsections = value;
	    				$.each(subsections, function(key, value){
	    					if (key == "subsection") {
	    						subsection = value;
	    						$.each(subsection, function(index, value){
	    							subSectionIndex = index;
	    							var questions = value;
	    							$.each(questions, function(key, value){
	    								if (key == "questions") {
	    									$.each(value, function(index, value){
	    										console.log(value.id, value.status);
	    										/*if(value.status) {
	    											octopus.nextQuestion();
	    										}*/
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

	    	return questionsArray;
	    },

		// todo fix MVC pattern issue
		ProgressButtonsBar : function() {
			for (var i=1; i<=37; i++){
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
			if (q.responseAnswer == "skip")
				q.status = "skip";
			else
				q.status = "submitted";
			q.responseTime = (responseTS - appearedTS) / (1000 * 60);
			// call server side submit function
            // creating json file for submit response
                //var data = {"currentQuestion": q.id, "submittedans":responseAnswer,"responsetime":q.responseTime,"stat"}
                data=JSON.stringify(q);
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
                testProgressView.init();
			// render question view
			// render test progress
		},

		getStatus : function() {
			return quizModel.quizState;
		},

		getCurrentQuestion : function() {
			console.log("current question called with " + quizModel.questionIndex);
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
			testProgressView.render();

		}
	};

	var testProgressView = {

		init : function() {
			this.pageTitle = $(".title");
			this.subSection = $("#h4");
			this.progressBar = $("#buttonBar");
			// initialize the test progress view
			this.render();
		},

		render : function() {

			// render the test progress view
			this.pageTitle.html(octopus.getQuizTitle());
			this.subSection.html(octopus.getQuizSubsection());
			
			this.qarray = octopus.getQuestions();
			this.progressBar.html("");
			$.each(this.qarray, function(index, value){
				if(!value.status) {
					testProgressView.progressBar.append(
						'<button type="button" id="' + (index + 1) +
						'" class="btn btn-default btn-xs">' + (index + 1) +
						'</button>&nbsp;');
				} else if (value.status == "skip") {
					testProgressView.progressBar.append(
						'<button type="button" id="' + (index + 1) +
						'" class="btn btn-danger btn-xs">' + (index + 1) +
						'</button>&nbsp;');
				} else if (value.status == "submitted") {
					testProgressView.progressBar.append(
						'<button type="button" id="' + (index + 1) +
						'" class="btn btn-success btn-xs">' + (index + 1) +
						'</button>&nbsp;');
				}
			});
			
			// var i=1;
			//  if(!this.qarray[i-1].status)
			 	
			//  if(this.qarray[i-1].status == "skipped")
			//  	$("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-warning btn-xs">'+i+'</button>&nbsp;');
			//  if(this.qarray[i-1].status == "submitted")
			//  	$("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-success btn-xs">'+i+'</button>&nbsp;');
			//  if(i-1==quizModel.questionIndex+1)
			//  	$("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-info btn-xs">'+i+'</button>&nbsp;');

			// for( i=2;i<=this.qarray.length;i++)
			// {
			// 	//console.log(this.qarray[i]);
   //                if(this.qarray[i-1].status=="undefined")
   //                   $("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-default btn-xs">'+i+'</button>&nbsp;');
   //               if(this.qarray[i-1].status=="skipped")
   //                   $("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-warning btn-xs">'+i+'</button>&nbsp;');
   //               if(this.qarray[i-1].status=="submitted")
   //                   $("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-success btn-xs">'+i+'</button>&nbsp;');
   //               if(i-1==quizModel.questionIndex+1)
   //                   $("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-info btn-xs">'+i+'</button>&nbsp;');

			// }
			// todo fix the MVC pattern issue
		},

		ProgressButtonsBarUpdate : function() {
			var i=1;
			if(i==quizModel.questionIndex+1)
			{
				$("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-info btn-xs">'+i+'</button>&nbsp;');
			    i++;
		    }
		    else 
		    {
			    $("#buttonBar").html('<button type="button" id="'+i+'" class="btn btn-success btn-xs">'+i+'</button>&nbsp;');
			    i++;
		    }

			for (i; i<quizModel.questionIndex+1; i++){
				$("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-success btn-xs">'+i+'</button>&nbsp;');
			}
			if(i==quizModel.questionIndex+1)
			{
				$("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-info btn-xs">'+i+'</button>&nbsp;');
				i++;
			}
			for (i; i<=30; i++){
				$("#buttonBar").append('<button type="button" id="'+i+'" class="btn btn-default btn-xs">'+i+'</button>&nbsp;');
				//$("#"+i).addClass('disabled');
			}

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
				if (selectedAnswer!="skip" && subsection.types == "essay")
						selectedAnswer = $("textarea").val();
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
				//console.log("cq"+currentQuestion.id);
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
