import click
from config import Config
from ai_assistant import AIAssistantV15

@click.group()
def cli():
    pass

@cli.command()
@click.option('--project-root', default='.', help='项目根目录')
def build_ir(project_root):
    from ir_extractor import MinimalIR
    ir = MinimalIR(project_root)
    ir.build()
    click.echo(f"✅ IR 构建完成，共 {len(ir.symbols)} 个函数。")

@cli.command()
@click.option('--project-root', default='.', help='项目根目录')
@click.option('--language', default='python', help='编程语言')
@click.argument('intent')
def generate(project_root, language, intent):
    config = Config(project_root=project_root)
    assistant = AIAssistantV15(config)
    code = assistant.generate_code(intent, language)
    click.echo("```\n" + code + "\n```")

if __name__ == '__main__':
    cli()