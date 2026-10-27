# Horizon 
https://www.philonewsletter.xyz 

## About 
We need more wisdom from the past to navigate the future. 

That’s the central thesis behind Horizon — an AI-powered weekly newsletter that compiles the week’s most pressing developments and opinions, and places it in conversation with the theories of relevant political philosophers and historians. Think about Trump’s rhetoric in the US-Iran war, and see it through the lens of Thucydides who spoke of “might makes right” dynamics in the Melian Dialogue. Or consider how Marx’s arguments have become more relevant in the age of AI: A new means of production wielded by powerful elite to extract surplus value from workers. 

This website is my attempt at building a crystal ball to see the future. I hope that through seeing the world through the lenses of historians and political philosophers, we would collectively emerge more informed, wiser and maybe even more creative in the way we frame the problems of today.

## Technical Architecture 
(1) A cron job using GitHub Actions is scheduled once every 7 days. This kickstarts the entire pipeline that culminates in the release of one article. 
(2) Backend calls the TinyFish Fetch API to fetch relevant articles from the week. This is cached in Redis, and then pushed to Postgres to minimise number of successful TinyFish API calls required. 
(3) This gets passed through another LLM, where it summarises the article and places it in conversation with a relevant historian or political philosopher. This final commentary is again stored in Postgres. 
(4) The article gets published on philonewsletter.xyz. 
(5) [in-progress] The article gets sent to a mailing list via Resend. 

Tech Stack: TinyFish, ChatGPT, Gemini, Next.js, React, Neon (Postgres), Resend