import argparse
import gradio as gr

from inference.checkpoint_inspector import CheckpointInspector
from cli.common import add_device_args
from logger import logger


class UI:
    def __init__(
        self,
        *,
        checkpoint_path=None,
        hf_checkpoint_path=None,
        device=None,
        dtype=None,
        title='Chat',
        description='Test the instruct checkpoint',
        debug=False
    ):
        self.inspector = CheckpointInspector(
            checkpoint_path = checkpoint_path,
            hf_checkpoint_path = hf_checkpoint_path,
            device=device,
            dtype=dtype
        )
        self.system_prompt = self.inspector.config.prompts.system_prompt
        self.title = title
        self.description = description
        self.iface = None
        self.debug = debug

    def normalize_history(self, history):
        # Gradio ChatInterface returns text messages as:
        # {'role': ..., 'content': [{'type': 'text', 'text': ...}], ...}
        return [{'role': h['role'], 'content': h['content'][0]['text']} for h in history]

    def chat_interface(
        self,
        message: str,
        history: list[dict],
        system_prompt: str,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
    ) -> str:
            if self.debug:
                logger.info(f'HISTORY: {history}')
                logger.info(f'MESSAGE: {message}')
            
            messages = [{'role': 'system', 'content': system_prompt}]
            messages.extend(self.normalize_history(history))
            messages.append({'role': 'user', 'content': message})

            outputs = self.inspector.generate(
                [messages],
                max_gen_len=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                use_kv_cache=True,
                instruct=True,
                full_seq=False,
                print_text=False,
                prompts_are_messages=True,
            )

            return outputs[0]['result_decoded']

    def init_ui(self, *, server_name='localhost', server_port=6006, share=False):
        logger.set_master(True)

        gr.close_all()
        if self.iface is not None:
            self.iface.close()
        
        self.iface = gr.ChatInterface(
            fn=self.chat_interface,
            title=self.title,
            description=self.description,
            chatbot=gr.Chatbot(height=600),
            textbox=gr.Textbox(
                placeholder='Message...',
                container=False,
            ),
            additional_inputs=[
                gr.Textbox(
                    value=self.system_prompt,
                    label='System prompt',
                    lines=3,
                    max_lines=8,
                ),
                gr.Slider(
                    minimum=16,
                    maximum=1024,
                    value=256,
                    step=16,
                    label='Max new tokens',
                ),
                gr.Slider(
                    minimum=0.0,
                    maximum=1.5,
                    value=0.0,
                    step=0.05,
                    label='Temperature',
                ),
                gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=1.0,
                    step=0.05,
                    label='Top p',
                ),
            ],
            fill_height=True,
            flagging_mode='never',
            save_history=False
        )

        self.iface.launch(share=share, server_name=server_name, server_port=server_port)

    def close_ui(self):
        gr.close_all()
        if self.iface is not None:
            self.iface.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gradio Serve Script Options')

    checkpoint_group = parser.add_mutually_exclusive_group(required=True)
    checkpoint_group.add_argument('--checkpoint', type=str, help='Checkpoint file path to load.')
    checkpoint_group.add_argument('--hf-checkpoint', type=str, help='Hugging Face model id or checkpoint path to load.')

    add_device_args(parser)

    parser.add_argument('--server-name', type=str, default='127.0.0.1')
    parser.add_argument('--server-port', type=int, default=6006)
    parser.add_argument('--share', action='store_true', help='Creates a public tunnel link so anyone with the link can test the checkpoint.')
    parser.add_argument('--debug', action='store_true', help='Enables debug logging.')

    parser.add_argument('--title', type=str, default='Chat')
    parser.add_argument('--description', type=str, default='Chat with the checkpoint')

    args = parser.parse_args()

    chat_ui = UI(
        checkpoint_path=args.checkpoint,
        hf_checkpoint_path=args.hf_checkpoint,
        device=args.device,
        dtype=args.dtype,
        title=args.title,
        description=args.description,
        debug=args.debug
    )

    try:
        chat_ui.init_ui(
            server_name=args.server_name,
            server_port=args.server_port,
            share=args.share
        )
    finally:
        chat_ui.close_ui()
