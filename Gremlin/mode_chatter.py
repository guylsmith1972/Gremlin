from configuration import get_config
import command_handler
import llama
import runtime

__instructions = ''

def process_transcript(full_transcript):
    transcript, parts = command_handler.parse(full_transcript)
       
    if len(parts) < 1 + (0 if runtime.command_prefix is None else 1):
        return
    
    args = parts[1:] if runtime.command_prefix is None else parts[2:]
    command = parts[0] if runtime.command_prefix is None else parts[1]
        
    if runtime.command_prefix is None or parts[0] == runtime.command_prefix:
        if not command_handler.execute(transcript, command, args, modeswitch_only=True):
            query = '\n'.join(full_transcript)
            if __instructions is not None and len(__instructions) > 0:
                query += '\n\n'
                query += f'Respond to the above transcript in accordance with the following instructions: {__instructions}'
                print('-' * 79)
                print(f'Subitting to LLM: {query}')
                print('-' * 79)
                response = llama.query_llm(query)
                print(response)
                print('-' * 79)


def set_instructions(instructions):
    global __instructions
    __instructions = instructions
    print(f'Chatter instructions: {__instructions}')
    