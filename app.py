import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Ensure parent dir on path so we can import gem_optimizer from workspace root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gem_optimizer

app = Flask(__name__)
app.secret_key = "change-me"


def serialize_results(results):
    """Convert Gem objects and results into JSON-serializable dicts for templates."""
    out = {
        'ancient': [],
        'reliquia': [],
        'legendary': [],
        'total_op': results.get('total_op', 0),
        'total_value': results.get('total_value', 0.0),
        'errors': results.get('errors', []),
    }

    for core in results.get('ancient', []):
        out['ancient'].append({
            'index': core['index'],
            'wp': core['wp'],
            'op': core['op'],
            'value': core['value'],
            'max_wp': core['max_wp'],
            'gems': [
                {'id': g.id, 'wp': g.wp, 'op': g.op, 'add_damage': g.add_damage, 'atk_power': g.atk_power, 'boss_dmg': g.boss_dmg}
                for g in core['gems']
            ]
        })

    for core in results.get('reliquia', []):
        out['reliquia'].append({
            'index': core['index'],
            'wp': core['wp'],
            'op': core['op'],
            'value': core['value'],
            'max_wp': core['max_wp'],
            'gems': [
                {'id': g.id, 'wp': g.wp, 'op': g.op, 'add_damage': g.add_damage, 'atk_power': g.atk_power, 'boss_dmg': g.boss_dmg}
                for g in core['gems']
            ]
        })

    for core in results.get('legendary', []):
        out['legendary'].append({
            'index': core['index'],
            'wp': core['wp'],
            'op': core['op'],
            'value': core['value'],
            'max_wp': core['max_wp'],
            'gems': [
                {'id': g.id, 'wp': g.wp, 'op': g.op, 'add_damage': g.add_damage, 'atk_power': g.atk_power, 'boss_dmg': g.boss_dmg}
                for g in core['gems']
            ]
        })

    return out


@app.route('/', methods=['GET'])
def index():
    # Pre-fill gems textarea with previously saved gems from session (if any)
    default_gems = session.get('gems_text', '')
    return render_template('index.html', default_gems=default_gems)


@app.route('/optimize', methods=['POST'])
def optimize():
    gem_lines = request.form.get('gems', '').strip().splitlines()
    try:
        num_ancient = int(request.form.get('num_ancient', '0'))
        num_reliquia = int(request.form.get('num_reliquia', '0'))
        num_legendary = int(request.form.get('num_legendary', '0'))
    except ValueError:
        flash('Enter integer values for core counts', 'error')
        return redirect(url_for('index'))

    optimizer = gem_optimizer.GemOptimizer()

    gem_id = 0
    for line in gem_lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 5:
            flash(f'Invalid gem line: "{line}". Use: WP OP AddDamage AtkPower BossDmg', 'error')
            return redirect(url_for('index'))
        try:
            wp = int(parts[0])
            op = int(parts[1])
            add_damage = int(parts[2])
            atk_power = int(parts[3])
            boss_dmg = int(parts[4])
        except ValueError:
            flash(f'Invalid numbers in line: "{line}"', 'error')
            return redirect(url_for('index'))

        optimizer.gems.append(gem_optimizer.Gem(wp=wp, op=op, add_damage=add_damage, atk_power=atk_power, boss_dmg=boss_dmg, id=gem_id))
        gem_id += 1

        # Persist the raw gems text in the user's session so the form can be pre-filled next time
        session['gems_text'] = request.form.get('gems', '')

    # Minimum gems required: Ancient and Reliquia need exactly 4 each, Legendary can use as few as 1
    min_needed = (num_ancient + num_reliquia) * optimizer.gems_per_core + num_legendary * 1
    if len(optimizer.gems) < min_needed:
        flash(f'Not enough gems: need at least {min_needed} (legendary can use 1), have {len(optimizer.gems)}', 'error')
        return redirect(url_for('index'))

    results = optimizer.optimize_cores(num_ancient, num_reliquia, num_legendary)
    view = serialize_results(results)

    return render_template('results.html', results=view)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
