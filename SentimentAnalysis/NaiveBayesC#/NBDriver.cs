/*
	Name: Elizabeth Brooks
	Date Modified: 06/22/2015
	File: NaiveBayesJAVA (NBDriver)
*/

//PreProcessor Directives
using System;

//Namespace (collection of classes)
namespace NaiveBayesClassifier
{
	//Class declaration (program file name may differ)
	class Driver
	{
		//The "main" method
		static void main(string[]args)
		{
			//Create a table to store input data
			DataTable table = new DataTable();
			//Add columns for data organization
			table.Columns.Add("Sentiment"); //Implicit String data type
			table.Columns.Add("Feature"); //Implicit String data type
			//Training data input
			//TO-DO
			//Classify the data
			Classifier classifier = new Classifier();
			classifier.TrainClassifier(table);
			//Output
			Console.WriteLine(classifier.Classify());
			Console.Read();
		}//End method main
	}//End class Driver
}//End namespace NaieveBayesClassifier