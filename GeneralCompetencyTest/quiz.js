	<script type="text/javascript">
	var quizdata;
	$.getJSON('quizdata.json', function(json) {
		quizdata = json;

		// display title of the page
		console.log(json.name);

		// populate the subsections of the quiz
		// loop through the sections to populate the dropdown
		console.log(json.section[0].name);

    });

	// on select of the section from the dropdown
	// load the questions into the following variable
	// show the first question with the continue button
	var questions;
</script>
