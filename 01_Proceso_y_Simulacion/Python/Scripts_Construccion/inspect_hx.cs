using System;
using System.IO;
using System.Xml.Serialization;
using DWSIM.UnitOperations.UnitOperations;
using DWSIM.Drawing.SkiaSharp.GraphicObjects.Shapes;

class Program
{
    static void Main()
    {
        try {
            var hx = new HeatExchanger();
            Console.WriteLine("HeatExchanger created successfully!");
            Console.WriteLine("Type: " + hx.GetType().FullName);
            Console.WriteLine("CalcMode: " + hx.CalcMode);

            var hxg = new HeatExchangerGraphic();
            Console.WriteLine("HeatExchangerGraphic created successfully!");
            Console.WriteLine("Type: " + hxg.GetType().FullName);
            Console.WriteLine("InConnectors: " + hxg.InputConnectors.Count);
            Console.WriteLine("OutConnectors: " + hxg.OutputConnectors.Count);
            for (int i = 0; i < hxg.InputConnectors.Count; i++) {
                Console.WriteLine($"  InputConnector {i}: ConnType={hxg.InputConnectors[i].ConnType}");
            }
            for (int i = 0; i < hxg.OutputConnectors.Count; i++) {
                Console.WriteLine($"  OutputConnector {i}: ConnType={hxg.OutputConnectors[i].ConnType}");
            }
        } catch (Exception ex) {
            Console.WriteLine("Error: " + ex);
        }
    }
}
