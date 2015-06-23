/*
	Name: Elizabeth Brooks
	Date Modified: 06/22/2015
	File: NaiveBayesC# (Classifier)
*/

//PreProcessor Directives
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data;

//Namespace (collection of classes)
namespace NaiveBayesClassifier
{
	//Class declaration (program file name may differ)
	class Classifier
	{
		//Class fields
		private DataSet dataSet = new DataSet();
		//Method to define the DataSet
		public DataSet DataSet
		{
			get{return dataSet;}
			set{dataSet = value;}
		}//End method
		//Method for training the data
		public void TrainClassifier(DataTable table)
		{
			//Add the created table to the dataSet
			dataSet.Tables.Add(table);
			//Create a table using a GaussianDistribution (normal distribution, by mean and variance)
			DataTable gaussianDistribution = dataSet.Tables.Add("Gaussian");
			gaussianDistribution.Columns.Add(table.Columns[0].ColumnName);
			//Add the columns
			for(int i=1; i<table.Columns.Count; i++){
				gaussianDistribution.Columns.Add(table.Columns[i].ColumnName + "Mean");
				gaussianDistribution.Columns.Add(table.Columns[i].ColumnName + "Variance");
			}//End for
			//Calc the number of appearances of specified sentiment or word (by table column)
			//var is used for a "strongly typed" implicit data type
			var results = (from myRow in table.AsEnumerable()
							group myRow by myRow.Field,String.(table.Columns[0].ColumnName) into grouping
							select new {Name = grouping.Key, count = grouping.Count()}).ToList();
			//Create tables for the rows
			for(int j=0; j<results.Count; j++){
				DataRow tableRow = gaussianDistribution.Rows.Add();
				//Set the rows to the results var
				tableRow[0] = results[j].Name;
				//Add the rows (by column)
				int counter = 1;
				for(int k=0; k<table.Columns.Count; k++){
					//save the results of calculations by the Helper class into a row of the DataRow object
					tableRow[counter] = Helper.Mean(SelectRows(table, k, string.Format("{0} = '{1}'", 
													table.Columns[0].ColumnName, results[j].Name)));
					//Pre-Increment the counter and save the results of calculations by the Helper class
					tableRow[++counter] = Helper.Variance(SelectRows(table, k, string.Format("{0} = '{1}'", 
															table.Columns[0].ColumnName, results[j].Name)));
					//Increment the counter again so it will be ready for the next iteration of the inner for loop
					counter++;
				}//End inner for
			}//End outer for
		}//End method TrainClassifier
		//Method for classifying strings
		public string Classify(double[]obj)
		{
			//Initialize the dictionary
			Dictionary<string, double> score = new Dictionary<string, double>();
			//var is used for a "strongly typed" implicit data type
			var results = (from myRow in dataSet.Tables[0].AsEnumerable()
							group myRow by myRow.Field<string>(dataSet.Tables[0].Columns[0].ColumnName) into grouping
							select new {Name = grouping.Key, Count = grouping.Count()}).ToList();
			//Loop through (by number of results) and create Lists to store the mean, variance, and results
			for(int i=0; i<results.Count; i++){
				List<double> subScoreList = new List<double>();
				int a=1, b=1;
				//For each item in the List (by "Gaussain" column), re-calc the mean, variance, and result
				for(int j=1; j<dataSet.Tables["Gaussian"].Columns.Count; j=j+2){
					double mean = Convert.ToDouble(dataSet.Tables["Gaussian"].Rows[i][a]);
					double variance = Convert.ToDouble(dataSet.Tables["Gaussian"].Rows[i][++A]);
					double result = Helper.NormalDist(obj[b-1], mean, Helper.SquareRoot(variance));
					subScoreList.Add(result);
					a++;b++;
				}//End first inner for
				//Calc the final score
				double finalScore = 0;
				for(int k=0; k<subScoreList.Count; k++){
					if(finalScore == 0){
						finalScore = subScoreList[k];
						continue;
					}//End if
					finalScore = finalScore*subScoreList[k];
				}//End second inner for
				score.Add(results[i].Name, finalScore*0.5);
			}//End outer for
			//Get the max score
			double maxOne = score.Max(c => c.Value);
			var name = (from c in score 
						where c.Value == maxOne 
						select c.Key).First();
			//Return the key corresponding to the max value
			return name;
		}//End method Classify
		//Helper functions
		#region Helper Functions
		//Helper function for selecting specific rows
		public IEnumerable<double> SelectRows(DataTable table, int column, string filter)
		{
			//Create a list of doubles to store the selected rows values
			List<double> doubleList = new List<double>();
			DataRow[] rows = table.Select(filter);
			for(int i=0; i<rows.Length; i++){
				doubleList.Add((double)rows[i][column]);
			}//End for
			return doubleList;
		}//End method SelectRows
		//Helper function to clear a dataSet
		public void clear()
		{
			dataSet = new DataSet();
		}//End method clear
		#endregion
	}//End class Classifier
}//End namespace NaiveBayesClassifier