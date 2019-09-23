function check_coordinates(array)
{
	if(array.constuctor.name == 'Array')
		if(0 in array && array[0].constuctor.name == 'Array')
			if(0 in array &&  array[0][0].constuctor.name == 'Number')
				return true;
	return false;
}

eel.expose(draw_point);
function draw_point(vertices, fill='#ff0000', pointSize=2)
{
	if(check_coordinates(vertices) || 1)
	{
		const canvas = document.getElementById('canvas');
		const context = canvas.getContext('2d');
		context.fillStyle = fill;
		for(var v=0; v in vertices; v++)
		{
			context.beginPath();
			context.arc(vertices[v][0], vertices[v][1], pointSize, 0, 2*Math.PI, true);
			context.fill();
		}
	}
}

eel.expose(draw_line);
function draw_line(vertices, fill='#ff0000', lineWidth=2)
{	
	if(check_coordinates(vertices) || 1)
	{
		const canvas = getElementById('canvas');
		const context = canvas.getContext('2d');
		context.fill = fill;
		for(var v = 0; v in vertices; v++)
		{
			context.beginPath();
			context.moveTo(vertices[v][0][0], vertices[v][0][1]);
			context.lineTo(vertices[v][1][0], vertices[v][1][1]);
			context.lineWidth = lineWidth;
			context.stroke();
		}
	}
}

eel.expose(draw_polygon);
function draw_polygon(vertices, color='#888888')
{
	if(check_coordinates(vertices) || 1)
	{
		const canvas = document.getElementById('canvas');
		const context = canvas.getContext('2d');
		context.fill = color;
		for(var v=0; v < verteces.length - 1; v++)
		{
			context.beginPath();
			context.moveTo(vertices[v][0], vertices[v][1]);
			context.moveTo(vertices[v+1][0], vertices[v+1][1]);
		}
			context.closePath();
			context.fill();
	}
}

eel.expose(get_canvas_size);
function get_canvas_size()
{
	const canvas = document.getElementById('canvas');
	return [canvas.width, canvas.height];
}

