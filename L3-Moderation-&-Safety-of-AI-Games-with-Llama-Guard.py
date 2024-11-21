#!/usr/bin/env python
# coding: utf-8

# # L3: Moderation & Safety of AI Games with Llama Guard
# 
# You are going to learn how to use Together AI's API to ensure content generated within AI games adheres to safety and compliance policies.

# <p style="background-color:#f7fff8; padding:15px; border-width:3px; border-color:#e0f0e0; border-style:solid; border-radius:6px"> 🚨
# &nbsp; <b>Different Run Results:</b> The output generated by AI models can vary with each execution due to their dynamic, probabilistic nature. Don't be surprised if your results differ from those shown in the video.<br>
# <span style="font-size: larger;">To maintain consistency, the notebooks are run with a 'world state' consistent with the video at the start of each notebook.</span></p>

# <div style="background-color:#fff6ff; padding:13px; border-width:3px; border-color:#efe6ef; border-style:solid; border-radius:6px">
# <p> 💻 &nbsp; <b>Access <code>requirements.txt</code> and <code>helper.py</code> files:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Open"</em>.
# 
# <p> ⬇ &nbsp; <b>Download Notebooks:</b> 1) click on the <em>"File"</em> option on the top menu of the notebook and then 2) click on <em>"Download as"</em> and select <em>"Notebook (.ipynb)"</em>.</p>
# 
# <p> 📒 &nbsp; For more help, please see the <em>"Appendix – Tips, Help, and Download"</em> Lesson.</p>
# 
# </div>

# ## Performing Safety Checks with the Default Content Policy

# In[ ]:


import os
from together import Together
from helper import get_together_api_key, load_env

client = Together(api_key=get_together_api_key())


# In[ ]:


from helper import get_game_state

game_state = get_game_state()
character = game_state["character"]
print("Character Description:", character)


# In[ ]:


safety_check = client.chat.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    messages=[{"role": "user", "content": character}],
)

print(f"prompt safety check: {safety_check.choices[0].message.content}")
print(" ")


# ### Safe Content Policy

# In[ ]:


# Set the content policy
safe_content_policy = {
    "policy": """O1: Violence and Hate.
Should not
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics.
- Use slurs based on personal characteristics
- Write gruesome / graphic violence.
Can
- Write tame fantasy violence
O2: Sexual Content.
Should not
- Write any somewhat sexual content that mentions sexual functions or sexual body parts.
- Write any content that would be inappropriate for kids.
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Write story depicting suicide.
O4: Profanity.
Should not
- Write with any profane language that wouldn't be appropriate for kids.
Can
- Write with kid appropriate language
O5: Regulated or Controlled Substances.
Should not
- Write stories that depicts, glorifies or encourages drug use."""
}


# In[ ]:


check_text = "Kill the troll."

prompt = f"""[INST] Task: Check if there is unsafe content in 'user' messages in conversations according to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{safe_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

print(prompt)


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Moderate Content Policy

# In[ ]:


# Set the content policy
moderate_content_policy = {
    "policy": """01: Violence and Hate
Should not
- Express racist, or offensive statements or slurs about people based on sensitive personal characteristics.
- Write graphics depicitions of gore that would make people very uncomfortable.
Can
- Write about violence or hate in a storytelling context.
O2: Sexual Content.
Should not
- Write sexually explicity content.
- Use any vulgar / sexual language
Can
- Write romantic content (including kissing, flirting etc...)
O3: Self-Harm.
Should not
- Encourage, or glorify self-harm or suicide."""
}


# In[ ]:


# Write the text you want to use to check whether the content policy is working
check_text = "Kill the troll."

# Build the prompt with embedded values
prompt = f"""[INST] Task: Check if there is unsafe content in 'user' messages in conversations according to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{moderate_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Mature Content Policy

# In[ ]:


# Set the content policy
mature_content_policy = {
    "policy": """O2: Sexual Content.
Should not
- Write about graphic or illegal content.
Can
- Write about mature content between adults"""
}


# In[ ]:


check_text = "Kill the troll."

prompt = f"""[INST] Task: Check if there is unsafe 
content in 'user' messages in conversations according 
to our safety policy with the below categories.

<BEGIN UNSAFE CONTENT CATEGORIES>
{mature_content_policy['policy']}
<END UNSAFE CONTENT CATEGORIES>

<BEGIN CONVERSATION>
user: {check_text}

Provide your safety assessment for user in the above conversation:
- First line must read 'safe' or 'unsafe'.
- If unsafe, a second line must include a comma-separated list of 
violated categories. [/INST]"""


# In[ ]:


response = client.completions.create(
    model="Meta-Llama/LlamaGuard-2-8b",
    prompt=prompt,
)
print(response.choices[0].text)


# ### Define helper functions

# In[ ]:


def is_safe (message):
    prompt = f"""[INST] Task: Check if there is unsafe content in 
    'user' messages in conversations according to our safety policy 
    with the below categories.
    
    <BEGIN UNSAFE CONTENT CATEGORIES>
    {safe_content_policy['policy']}
    <END UNSAFE CONTENT CATEGORIES>
    
    <BEGIN CONVERSATION>
    user: {message}
    
    Provide your safety assessment for user in the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of 
    violated categories. [/INST]"""

    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )

    result = response.choices[0].text
    return result.strip() == 'safe'


# In[ ]:


from helper import run_action, start_game, get_game_state

game_state = get_game_state()

def main_loop(message, history):

    if not is_safe(message):
        return 'Invalid action.'
    
    result = run_action(message, history, game_state)
    safe = is_safe(result)
    if(safe):
        return result # only if safe?
    else:
        return 'Invalid output.'

start_game(main_loop, True)


# In[ ]:





# In[ ]:




