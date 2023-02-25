using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace YourNamespace
{
    class Codex 
    {
        private readonly HttpClient _client;
        private readonly string _apiKey;

        public Codex(string apiKey)
        {
            _client = new HttpClient();
            _apiKey = apiKey;
        }

        public async Task<string> GenerateCode(string prompt, string language, int maxTokens)
        {
            var content = new StringContent($"{{\"prompt\": \"{prompt}\", \"model\": \"text-codex-002\", \"temperature\": 0.7, \"max_tokens\": {maxTokens}, \"stop\": [\"\\n\"]}}", Encoding.UTF8, "application/json");
            _client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", _apiKey);
            var response = await _client.PostAsync($"https://api.openai.com/v1/codex/completions?model={language}", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            return responseContent;
        }
    }
}