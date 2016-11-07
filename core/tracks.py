import json
import copy


def format_tracks_data(data, total_frame, total_time):
    pre_list = []
    res = []
    json_data = json.loads(data)
    for k, v in json_data.iteritems():
        size = v.get('size')
        if size < 0:
            size = 144
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
            if df > 0:
                dt = (total_time - itm.get('time')) / df
                for i in range(1, df + 1):
                    nt = copy.deepcopy(itm)
                    nt['frame'] += i
                    nt['time'] += dt * i
                    res.append(nt)
        else:
            if n == 0:
                df = itm.get('frame')
                if df != 1:
                    dt = (itm.get('time')) / (df - 1)
                    st = copy.deepcopy(itm)
                    st['time'] = 0
                    for i in range(0, df - 1):
                        nt = copy.deepcopy(st)
                        nt['time'] += dt * i
                        nt['size'] = 0
                        nt['frame'] = i + 1
                        res.append(nt)
            nitm = pre_list[n + 1]
            hidden = False
            df = float(nitm.get('frame') - itm.get('frame'))
            dx = (nitm.get('x') - itm.get('x')) / df
            dy = (nitm.get('y') - itm.get('y')) / df
            ds = (nitm.get('size') - itm.get('size')) / df
            if nitm.get('size') == 0:
                ds = 0
            if itm.get('size') == 0:
                hidden = True
            dr = (nitm.get('rotation') - itm.get('rotation')) / df
            dt = (nitm.get('time') - itm.get('time')) / df
            for i in range(1, int(df)):
                if hidden:
                    s_dict = {'time': itm.get('time') + dt * i,
                              'x': itm.get('x') + dx * i,
                              'y': itm.get('y') + dy * i,
                              'size': 0,
                              'rotation': itm.get('rotation') + dr * i,
                              'frame': int(itm.get('frame') + i)}
                else:
                    s_dict = {'time': itm.get('time') + dt * i,
                              'x': itm.get('x') + dx * i,
                              'y': itm.get('y') + dy * i,
                              'size': itm.get('size') + ds * i,
                              'rotation': itm.get('rotation') + dr * i,
                              'frame': int(itm.get('frame') + i)}
                res.append(s_dict)

    res.sort(key=lambda x: x['frame'])
    res[-1]['time'] += 0.04
    return res
