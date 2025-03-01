#!/usr/bin/env python3

import yaml
import glob
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('readme')

notes = [
    # predicate, tag, description
]
container_rows = [
    '| **Name** | **Description** | **Ports** | **Links** |',
    '|---|---|---|---|'
]
container_template = '| [{}]({}) {} | {} | {} | {} |'

env_rows = [
    '| **Variable** | **Description** | **Example** |',
    '|---|---|---|'
]
env_template = '| {} | {} | {} |'

if __name__ == '__main__':
    for file_name in sorted(glob.glob('./stacks/**/docker-compose.*.yml', recursive=True)):
        with open(file_name, 'r') as f:
            try:
                compose = yaml.safe_load(f)
                logger.info(f'processing compose file {file_name}')
                for name, service in compose.get('services', {}).items():
                    labels = service.get('labels', {})

                    f.seek(0)
                    line_no = next(
                        num for num, line in enumerate(f, 1) 
                        if f'container_name: {name}' in line
                    )

                    tags = ','.join([
                        tag for (predicate, tag, _) in notes 
                        if predicate(service)
                    ])

                    container_rows.append(container_template.format(
                        name,
                        f'{file_name}#L{line_no}',
                        f'<sup>{tags}</sup>' if tags else '', 
                        labels.get('readme.description', ''),
                        ', '.join(map(
                            lambda p: f'`{p}`', 
                            service.get('ports', [])
                        )),
                        ', '.join(['[{}]({})'.format(label, 
                            labels.get(f'readme.links.{i}')) for label, i in [
                                ('GitHub', 'github'), 
                                ('GitLab', 'gitlab'),
                                ('Docker Hub', 'docker'), 
                                ('Website', 'web')
                            ] if f'readme.links.{i}' in labels])
                    ))
                count = len(compose.get('services', {}))
                logger.info(f'processed {count} services in {file_name}')
            except yaml.YAMLError as e:
                logger.error('failed to parse yaml: ', e)

    containers = '\n'.join(container_rows) + '\n\n'
    containers += '\n\n'.join([f'<sup>{tag}</sup>{description}' for _, tag, description in notes])

    for file_name in sorted(glob.glob('.env.*')):
        logger.info(f'processing variables in {file_name}')
        comment = str()
        example = str()
        count = 0
        with open(file_name, 'r') as f:
            for line in filter(lambda v: v.strip(), f.readlines()):
                if line.startswith('# ex: '):
                    example = line.removeprefix('# ex: ').strip()
                elif line.startswith('#'):
                    comment = line.strip('# ').strip()
                else:
                    value = line.split('=')[0]
                    env_rows.append(env_template.format(
                        f'`{value}`', comment, f'`{example}`' if example else ''
                    ))
                    count += 1
                    comment = str()
                    example = str()
        logger.info(f'processed {count} variables in {file_name}')
    
    envs = '\n'.join(env_rows) + '\n'

    logger.info('reading README template')
    with open('README.tmpl.md', 'r') as f:
        readme = f.read().format(
            containers=containers,
            envs=envs
        )

        logger.info('writing new README')
        with open('README.md', 'w') as f2:
            f2.write(readme)

    logger.info('done...')

