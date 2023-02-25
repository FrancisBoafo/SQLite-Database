using System;
using System.Threading.Tasks;

namespace YourNamespace
{
    class Program
    {
        static async Task Main(string[] args)
        {
            string apiKey = "your_api_key";
            Codex codex = new Codex(apiKey);
            string prompt = "Sort an array in ascending order.";
            string language = "python";
            int maxTokens = 100;
            string code = await codex.GenerateCode(prompt, language, maxTokens);
            Console.WriteLine(code);
        }
    }
}
