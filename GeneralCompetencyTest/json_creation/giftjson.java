import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
public class giftjson {
	static ArrayList<json1> a=new ArrayList<json1>();
	static int i=0;
	public static void main(String[] args)
	{
		//String section="";
		System.out.println("enter the file name");
		Scanner in=new Scanner(System.in);
		String filename=in.nextLine();
		String content=readFile(filename);
		//System.out.println(content);
		for( i=0;i<content.length();i++)
		{
			json1 obj=new json1();
			//System.out.println("hi");
			while(content.charAt(i)!='*')
			{
				i++;
			}
			if(content.charAt(i)=='*')
			{
				//System.out.println("hi");
				while(content.charAt(i)=='*')
				{
					i++;
				}
				//System.out.println(i);
				while(content.charAt(i)!='*')
				{
					
				obj.section=obj.section+content.charAt(i);
				i++;
				}
			}
			if(i==content.length()-1)
				break;
			section(content,obj,obj.section);
						//break;
		
		}
		WriteToJson();
	}
	public static void section(String content,json1 obj,String s)
	{
		obj=new json1();
		obj.section=s;
		/*String section="",qid="",questn="",sid="",opt="";
		String []options;*/
		
		while(content.charAt(i)!=':')
		{
			i++;
		}
		if(content.charAt(i)==':')
		{
			i=i+2;
			while(content.charAt(i)!=':')
			{
			obj.qid=obj.qid+content.charAt(i);
			i++;
			}
		}
		
		if(content.charAt(i)==':')
		{
			i=i+2;
			while(content.charAt(i)!='-')
			{
			obj.sid=obj.sid+content.charAt(i);
			i++;
			}
		}
		i++;
		while(content.charAt(i)!='-')
		{
			i++;
		}
		if(content.charAt(i)=='-')
		{
			i++;
			while(content.charAt(i)!='{')
			{
				if(content.charAt(i)=='*')
					return;
			obj.questn=obj.questn+content.charAt(i);
			i++;
			}
		}
		if(content.charAt(i)=='{')
		{
			i++;
			while(content.charAt(i)!='}')
			{
			obj.opt=obj.opt+content.charAt(i);
			i++;
			}
		}
		obj.opt=obj.opt.trim();
		obj.options=obj.opt.split("\\n");
		if(content.charAt(i)=='*')
		{
			
		}
	
		System.out.println(obj.section);
		/*System.out.println(obj.qid);
		System.out.println(obj.sid.trim());*/
		//System.out.println(obj.questn.trim());
		/*System.out.println(obj.options[0]);
		System.out.println(obj.options[1]);
		System.out.println(obj.options[2]);
		System.out.println(obj.options[3]);*/
		System.out.println("----------");
		a.add(obj);
		//System.out.println(i+","+content.length());
		
		while(content.charAt(i)!='*' && content.charAt(i)!=':')
		{
			//System.out.println(i+","+content.length());
			if(i==content.length()-1)
			return;
			//System.out.println(content.charAt(i));
           i++;
		}
		//System.out.println(content.charAt(i));
		if(content.charAt(i)==':')
			section(content,obj,obj.section);
		else{
			//System.out.println(content.charAt(i));
		return;
		}
	}
	public static String readFile(String filename)
	{
	   String content = null;
	   File file = new File(filename); //for ex foo.txt
	   try {
	       FileReader reader = new FileReader(file);
	       char[] chars = new char[(int) file.length()];
	       reader.read(chars);
	       content = new String(chars);
	       reader.close();
	   } catch (IOException e) {
	       e.printStackTrace();
	   }
	   return content;
	}
	
	public static void WriteToJson()
	{
		JSONObject object=new JSONObject();
		JSONArray list2 = new JSONArray();
		for(int j=0;j<a.size();j++)
		{
		JSONObject obj = new JSONObject();
		
		json1 obj1=a.get(j);
		obj.put("section name", obj1.section);
		obj.put("section id", obj1.sid);
		obj.put("question id", obj1.qid);
		
		//obj.put("age", new Integer(100));
	 
		//JSONArray list1 = new JSONArray();
		JSONArray list1 = new JSONArray();
		//list1.add(obj1.questn);
		for(int i=0;i<obj1.options.length;i++)
		list1.add(obj1.options[i]);
		//list1.add(obj.put("options", list1));
		//list.add("msg 2");
		//list.add("msg 3");
	 
		obj.put("question", obj1.questn);
		obj.put("options", list1);
		list2.add(obj);
		}
		object.put("General Competancy Test", list2);
		try {
	 
			FileWriter file = new FileWriter("test.json");
			file.write(object.toJSONString());
			file.flush();
			file.close();
	 
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		//System.out.print(obj1);
		
	}
}

class json1
{
	String section,qid,questn,sid,opt;
	String []options;
	public json1()
	{
		this.section="";
		this.qid="";
		this.questn="";
		this.sid="";
		this.opt="";
		this.options=new String[10];
	}
}
