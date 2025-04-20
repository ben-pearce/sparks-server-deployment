#!/usr/bin/env python3

import glob
import logging
import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('readme')

CONTAINER_TEMPLATE = '| [{}]({}) {} | {} | {} | {} |'
ENV_TEMPLATE = '| {} | {} | {} |'

notes = [
    # predicate, tag, description
    (
        lambda s: any(
            v.startswith('${MEDIA_DIR}')
            for v in s.get('volumes', [])),
        '1',
        'Assumes mass storage available, mounted at MEDIA_DIR on the host.'
    ),
    (
        lambda s: s.get('network_mode', None) == 'service:tunnel',
        '2', 'All traffic is routed via tunnel VPN client container.'
    )
]

container_rows = [
    '| **Name** | **Description** | **Ports** | **Links** |',
    '|---|---|---|---|'
]

env_rows = [
    '| **Variable** | **Description** | **Example** |',
    '|---|---|---|'
]

if __name__ == '__main__':
    for file_name in sorted(
        glob.glob('./**/docker-compose*.yml', recursive=True)
    ):
        with open(file_name, 'r', encoding="utf-8") as f:
            try:
                compose = yaml.safe_load(f)
                logger.info('processing compose file %s', file_name)
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

                    container_rows.append(CONTAINER_TEMPLATE.format(
                        name,
                        f'{file_name}#L{line_no}',
                        f'<sup>{tags}</sup>' if tags else '',
                        labels.get('readme.description', ''),
                        ', '.join(map(
                            lambda p: f'`{p}`',
                            service.get('ports', [])
                        )),
                        ', '.join([
                            f'[{label}]({labels.get(f"readme.links.{i}")})'
                            for label, i in [
                                ('GitHub', 'github'),
                                ('GitLab', 'gitlab'),
                                ('Docker Hub', 'docker'),
                                ('Website', 'web')
                            ] if f'readme.links.{i}' in labels])
                    ))
                count = len(compose.get('services', {}))
                logger.info('processed %d services in %s', count, file_name)
            except yaml.YAMLError as e:
                logger.error('failed to parse yaml: %s', e)

    containers = '\n'.join(container_rows) + '\n\n'
    containers += '\n\n'.join([
        f'<sup>{tag}</sup>{description}'
        for _, tag, description in notes
    ])

    for file_name in sorted(glob.glob('.env.*')):
        logger.info('processing variables in %s', file_name)
        comment = str()
        example = str()
        count = 0
        with open(file_name, 'r', encoding="utf-8") as f:
            for line in filter(lambda v: v.strip(), f.readlines()):
                if line.startswith('# ex: '):
                    example = line.removeprefix('# ex: ').strip()
                elif line.startswith('#'):
                    comment = line.strip('# ').strip()
                else:
                    value = line.split('=')[0]
                    env_rows.append(ENV_TEMPLATE.format(
                        f'`{value}`', comment, f'`{example}`'
                        if example else ''
                    ))
                    count += 1
                    comment = str()
                    example = str()
        logger.info('processed %d variables in %s', count, file_name)

    logger.info('reading README template')
    with open('README.tmpl.md', 'r', encoding="utf-8") as f:
        readme = f.read().format(
            containers=containers,
            envs='\n'.join(env_rows) + '\n'
        )

        logger.info('writing new README')
        with open('README.md', 'w', encoding="utf-8") as f2:
            f2.write(readme)

    logger.info('done...')
