import json
import copy


def format_tracks_data(data, total_frame):
    pre_list = []
    res = []
    json_data = json.loads(data)
    for k, v in json_data.iteritems():
        size = v.get('size')
        if size < 0:
            size = 144
        elif size == 0:
            size = 1
        s_dict = {'time': float("{:.02f}".format(float(k))),
                  'x': v.get("x"),
                  'y': v.get("y"),
                  'rotation': v.get("rotation"),
                  'size': size,
                  'frame': v.get('frame')}
        pre_list.append(s_dict)

    pre_list.sort(key=lambda x: x['frame'])

    for n, itm in enumerate(pre_list):
        res.append(itm)
        if n == (len(pre_list) - 1):
            df = total_frame - itm.get('frame')
            for i in range(1, df + 1):
                nt = copy.deepcopy(itm)
                nt['frame'] += i
                res.append(nt)
        else:
            nitm = pre_list[n + 1]
            df = float(nitm.get('frame') - itm.get('frame'))
            dx = (nitm.get('x') - itm.get('x')) / df
            dy = (nitm.get('y') - itm.get('y')) / df
            ds = (nitm.get('size') - itm.get('size')) / df
            dr = (nitm.get('rotation') - itm.get('rotation')) / df
            dt = (nitm.get('time') - itm.get('time')) / df
            for i in range(1, int(df)):
                s_dict = {'time': itm.get('time') + dt * i,
                          'x': itm.get('x') + dx * i,
                          'y': itm.get('y') + dy * i,
                          'size': itm.get('size') + ds * i,
                          'rotation': itm.get('rotation') + dr * i,
                          'frame': int(itm.get('frame') + i)}
                res.append(s_dict)

    res.sort(key=lambda x: x['frame'])
    return res