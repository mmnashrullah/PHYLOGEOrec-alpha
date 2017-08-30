from math import *
import datetime

def get_lon_midpoint(lon1,lon2):
    #check to see if we are crossing the pm
    if 180 < (abs(lon1 - lon2)):
        #if yes, correct calculation of midpoint
        mid = 180-abs(lon1)
        mid += 180-abs(lon2)
        mid = mid/2
        if lon1 < lon2:
            lonm = lon1 - mid
        else:
            lonm = lon2 - mid
        if lonm<-180:
            lonm = lonm+360
    else:
        lonm = (lon1+lon2)/2
    return lonm

def get_linestring(lat0,lon0,alt0,lat1,lon1,alt1):
    #the number of linesegments
    steps = 20

    #latitude calculations
    lat_step = (lat1-lat0)/float(steps)
    lats = [lat0]
    ct = 1
    while ct < (steps-1):
        lats.append(lat0+(lat_step*ct))
        ct += 1
    lats.append(lat1)

    #altitude calculations
    alt_step = (alt1-alt0)/float(steps)
    alts = [alt0]
    ct = 1
    while ct < (steps-1):
        alts.append(alt0+(alt_step*ct))
        ct += 1
    alts.append(alt1)

    #longitude calculations including great circle
    # great circle if flag gets set to 1
    flag = 0
    if 180 < (abs(lon0 - lon1)):
        flag = 1
        t = 180-abs(lon0)
        t += 180-abs(lon1)
        lon_step = t/float(steps)
        if lon0<lon1:
            lon_step = lon_step * -1
    else:
        lon_step = (lon1-lon0)/float(steps)
        lons = [lon0]
        ct = 1
        while ct < (steps-1):
            lons.append(lon0+(lon_step*ct))
            ct += 1
        lons.append(lon1)


    if flag == 1:
        lons = [lon0]
        ct = 1
        while ct < (steps-1):
            cur = lon0+(lon_step*ct)
            if -180 < cur and cur < 180:
                lons.append(cur)
            elif cur < -180:
                over = (cur + 180)
                cur = 180 + over
                lons.append(cur)
            else:
                over = (cur - 180)
                cur = -180 + over
                lons.append(cur)
            ct += 1
        lons.append(lon1)

    ct = 0
    linestring = ''
    while ct < len(lats):
        linestring += str(lons[ct])+','+str(lats[ct])+','+str(int(alts[ct]))+' \n'
        ct+=1
    return linestring

def is_rooted(tree):
    pos = 0
    c = tree[pos]
    depth = 0
    comma = 0
    for pos in range(0,len(tree)):
        c = tree[pos]
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == ',':
            if depth == 1:
                comma += 1
    return comma == 1



#Build Leaf Nodes
class build_kml_leafnodes:
    def __init__(self,tree,coords,mydomain,branch_color,branch_width,node_url,alt_grow,proximity,kml_title):
        tree = tree.replace('\n','')
        tree = tree.strip()

        if tree[-1] == "," or tree[-1] == ";":
            tree = tree[0:-1]

        err = False
        typeX = ""

        if tree.count('(') != tree.count(')'):
            err = True
            typeX += 'Your tree contains '+str(tree.count('('))+' open parenthesis "(" and '+str(tree.count(')'))+' close parenthesis ")" '+"\n"
            #return "",0,err,typeX

        if not is_rooted(tree):

            err = True
            typeX += "Your tree does not appear to be rooted. We attempted to force a root, but it may not be the same as you intended. \n If you are sure your tree was rooted, this probably didn't change anything.\n"
            tree = "("+tree+")"


        #variables:
        # proximity
        # alt_grow
        # internal_icon
        # default_color

        internal_icon = str(node_url)

        default_color = str(branch_color)

        alt_grow = int(alt_grow)

        #this sets the number of decimals to round coordinates to when
        #looking for points sharing the same location
        proximity = int(proximity)
        #set the radius size of the circle to scatter them around
        offset = (1*10**(-1*proximity))*.75

        coords = coords.strip()
        tree = tree.strip()

        coords = coords.split('\n')
        lat = {}
        lon = {}
        #track unique coords in order to implement scatter of those overlapping
        uniques = {}
        tstamps = False
        maxtime = datetime.datetime.min

        icons = {}
        for line in coords:
            if line != '':
                curr = line.split(';')
                if 3 <= len(curr):
                    lat[curr[0]] = float(curr[1].strip())
                    lon[curr[0]] = float(curr[2].strip())

                    title = str(round(float(curr[1]),proximity))+'_'+str(round(float(curr[2]),proximity))
                    n = 0
                    if title in uniques:
                        n = int(uniques[title])
                    uniques[title] = n + 1


                    if 4 <= len(curr):
                        if curr[3].strip() == '':
                            icons[curr[0]] = 'default'
                        else:
                            icons[curr[0]] = curr[3].strip()


                        #if datetime set in CSV, extract and store in dictionary
                        if 5 <= len(curr):
                            #date
                            #format= year-mm-day:hour:
                            if tstamps == False:
                                tstamps = {}
                            if len(str(curr[4].strip())) != 0:
                                curdate = curr[4].strip().split('-')
                                yr = int(curdate[0])
                                tmp_date = datetime.datetime(yr,01,01)
                                if 2 <= len(curdate):
                                    mn = int(curdate[1])
                                    tmp_date = tmp_date.replace(month = mn)
                                    if 3 <= len(curdate):
                                        daytime = curdate[2].split('T')
                                        dy = int(daytime[0])
                                        tmp_date = tmp_date.replace(day = dy)
                                        if 2 <= len(daytime):
                                            daytime = daytime[1].split(':')
                                            hr = int(daytime[0])
                                            tmp_date = tmp_date.replace(hour = hr)
                                            if 2 <= len(daytime):
                                                mt = int(daytime[1])
                                                tmp_date = tmp_date.replace(minute = mt)
                                                if 3 <= len(daytime):
                                                    sc = int(daytime[2])
                                                    tmp_date = tmp_date.replace(second = sc)
                                tstamps[curr[0]] = tmp_date
                                if maxtime < tmp_date:
                                    maxtime = tmp_date

                    else:
                        icons[curr[0]] = 'default'

        used_uniques = {}
        for i,t in uniques.items():
            if 1< int(t):
                used_uniques[i] = 0


        kml = tree
        leafs = [1,2,3,4]


        ancestor = ""
        cur_anc = 0
        leafs = {}
        nodes = {}
        rank = {}
        nodes[0]="root"
        cur_leaf = ""
        isleaf = False
        pos = 0
        c = tree[pos]
        depth = 0
        comma = 0
        maxdepth = 0
        rank = {}
        rank[cur_anc] = 0
        children = {}
        children[cur_anc] = []


        for pos in range(0,len(tree)):
            c = tree[pos]
            if c == '(':
                if isleaf and 0<len(cur_leaf):
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth += 1
                if maxdepth < depth:
                    maxdepth = depth
                last_anc = cur_anc
                cur_anc = 'HTU_'+str(len(nodes))
                children[cur_anc] = []
                nodes[cur_anc] = last_anc
                rank[cur_anc] = depth
                children[last_anc].append(cur_anc)
                isleaf=True
            elif c == ')':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth -= 1
                cur_anc = nodes[cur_anc]
                isleaf=False
            elif c == ',':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    rank[cur_leaf] = depth
                    leafs[cur_leaf] = cur_anc
                    children[cur_anc].append(cur_leaf)
                cur_leaf = ""
                isleaf = True
            elif c==":":
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                isleaf = False
                cur_leaf = ""
            elif isleaf:
                cur_leaf += c
                cur_leaf = cur_leaf.lstrip()

        if len(lat)<len(leafs) or len(lon)<len(leafs):
            err = True
            typeX += 'There seems to be something missing.'+str(len(leafs))+' tips existed in your tree and '+str(len(lat))+' lat and '+str(len(lon))+" lon existed\n"

        #this function scatters any points of shared radius = 'offset'
        #around a circle at equal distances
        #if timestamps were given, it also fills any black timestamps with the maxtime value
        for nm,anc in leafs.items():
            if tstamps != False:
                if nm not in tstamps:
                    tstamps[nm] = maxtime
            try:
                curla = float(lat[nm])
                curlo = float(lon[nm])
            except:
                err = True
                curlo = lon.items()[-1][1]
                curla = lat.items()[-1][1]
                typeX += "Not all leaf-nodes in your tree are found in your coordinates file. See, "+str(nm)+". For now we tried to just place this node at "+str(curla)+","+str(curlo)+". You'll have to go back and fix it\n"
                lat[nm] = curla
                lon[nm] = curlo

                #return "",0,error,typeX
            title = str(round(float(curla),proximity))+'_'+str(round(float(curlo),proximity))
            if title in used_uniques:
                total = uniques[title]
                used = int(used_uniques[title])

                #scatter points sharing lat/lon around a circle of radius = 'offset'

                angle = float(360)/(total)
                angle = radians(angle*used)
                tmpx = cos(angle) * offset
                tmpy = sin(angle) * offset
                tmpx += -offset
                tmpy += -offset
                tmp_lon = curlo + tmpx
                tmp_lat = curla + tmpy

                if tmp_lon < -180:
                    tmp_lon += 360
                elif 180 < tmp_lon:
                    tmp_lon += -360

                #still testing the scatter feature
                lat[nm] = round(float(tmp_lat),proximity)
                lon[nm] = round(float(tmp_lon),proximity)

                used_uniques[title] = used+1



        #rank = sorted(rank.items(),reverse=True)
        rankorder = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        lstring_flag = [] #used to later deterime if a branch is a rectangular cladogram
        altitude = {}

        for n,a in leafs.items():
            altitude[n] = 0


        #set the altitude,lat,lon for each internal node
        for n in rankorder:
            r = n[1]
            n = n[0]
            try:
                a = leafs[n]
                altitude[n] = 0.0
            except:
                child_list = children[n]
                max_alt = 0
                min_time = datetime.datetime.today()
                max_dist = 0
                child_count = len(child_list)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                ct = 0
                last_c = ""
                tot_lon = 0
                tot_lat = 0
                for c in child_list:
                    alt = altitude[c]
                    if max_alt<alt:
                        max_alt = alt
                    if tstamps != False:
                        if tstamps[c]<min_time:
                            min_time = tstamps[c]
                    curlat = float(lat[c])
                    curlon = float(lon[c])
                    if max_lat<curlat:
                        max_lat = curlat
                    if max_lon<curlon:
                        max_lon = curlon
                    if curlat<min_lat:
                        min_lat = curlat
                    if curlon<min_lon:
                        min_lon = curlon
                    tot_lon += curlon
                    tot_lat += curlat
                    ct+=1
                    last_c = c

                curlat = tot_lat/ct
                curlon = tot_lon/ct
                if curlon<-180:
                    curlon += 360
                if 180<curlon:
                    curlon -= 360
                """
                lat[n] = (max_lat + min_lat)/2
                lon[n] = get_lon_midpoint(max_lon,min_lon)
                lonvalue = min((max_lon-min_lon),(min_lon-(max_lon-360)))
                dist = sqrt(((lonvalue)**2) + ((max_lat-min_lat)**2))
                """
                lat[n] = float(curlat)
                lon[n] = float(curlon)
                max_dist = 0
                for c in child_list:
                    m1 = float(lon[n])
                    m2 = float(lon[c])
                    v = max(m1,m2)-min(m1,m2)
                    if v < -180:
                        v += 360
                    elif 180 < v:
                        v -=360
                    dist = sqrt(((v)**2) + ((lat[n]-lat[c])**2))
                    if dist <= 10.0:
                        lstring_flag.append(c)

                    if max_dist<dist:
                        max_dist = dist

                dist = max_dist
                if tstamps != False:
                    tstamps[n] = min_time

                new_alt = max_alt + (alt_grow * dist * .5) + alt_grow

                altitude[n] = int(new_alt)




        kml = '<?xml version="1.0" encoding="UTF-8"?>\n <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">>\n <Document>\n\t <name>&title</name>\n\t <open>1</open>\n\t <Snippet maxLines="2"></Snippet>\n'
        if err:
            kml += "\n<description><![CDATA[\n"
            kml += typeX
            kml += "\n]]></description>"
            kml = kml.replace('&title',"ERRORS")
        else:
            kml = kml.replace('&title',kml_title)

        highlight_branch_width = str(branch_width*2)
        branch_width = str(branch_width)
        style =  '\t<Style id="ICNUMa">\n' \
        '            <IconStyle>\n' \
        '                <scale>.25</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '                <scale>0</scale>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '        </Style>\n' \
        '        <Style id="ICNUMb">\n' \
        '            <IconStyle>\n' \
        '                <scale>.95</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+highlight_branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '            </Style>\n' \
        '         <StyleMap id="ICNUM">\n' \
        '            <Pair>\n' \
        '                <key>normal</key>\n' \
        '                <styleUrl>#ICNUMa</styleUrl>\n' \
        '            </Pair>\n' \
        '              <Pair>\n' \
        '                   <key>highlight</key>\n' \
        '                   <styleUrl>#ICNUMb</styleUrl>\n' \
        '              </Pair>\n' \
        '         </StyleMap>\n'


        kml += style.replace('ICURL',internal_icon).replace('ICNUM',str(0))

        used = {}
        used['default'] = 0
        styles = {}
        ct = 1
        for name,icon in icons.items():
            if icon in used:
                styles[name] = used[icon]
            else:
                kml += style.replace('ICURL',icon).replace('ICNUM',str(ct))
                styles[name] = ct
                used[icon] = ct
                ct+=1

        kml += '<Folder>\n <name>Leaf nodes</name>\n <open>0</open>\n'


        placemark = '    <Placemark>\n' \
        '        <name>PMNAME</name>\n' \
        '        PMTIMESTAMP' \
        '        <description><![CDATA[PMCDATA]]></description>\n' \
        '        <Snippet maxLines="2"></Snippet>\n' \
        '        <styleUrl>STURL</styleUrl>\n' \
        '        <Point id="pt_PMNAME">\n' \
        '            <extrude>0</extrude>\n' \
        '            <altitudeMode>relativeToGround</altitudeMode>\n' \
        '            <coordinates>PMLON,PMLAT,PMALT</coordinates>\n' \
        '        </Point>\n' \
        '    </Placemark>\n'
        timestamp = '<TimeStamp><when>pmtstamp</when></TimeStamp>'

        for p,anc in leafs.items():
            latitude = float(lat[p])
            longitude = float(lon[p])
            anc_lat = float(lat[anc])
            anc_lon = float(lon[anc])
            anc_alt = int(float(altitude[anc]))
            pm_color = default_color

            pm_cdata = '<body>'
            #build description window
            ahref = '<b>Ancestor: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(anc_lon)+'&lat='+str(anc_lat)+'&alt='+str(anc_alt)+'">'+str(anc)+'</a><br>'
            pm_cdata += ahref

            pm_cdata += '</body>'

            try:
                style = styles[p]
            except:
                style = styles.items()[-1][1]

            tstring = ''
            if tstamps != False:
                if p in tstamps:
                    ts = tstamps[p]
                    ts = ts.isoformat()
                    tstring = timestamp.replace('pmtstamp',str(ts))

            pm = placemark.replace('PMNAME',str(p))
            pm = pm.replace('PMTIMESTAMP',tstring)
            pm = pm.replace('PMLON',str(longitude))
            pm = pm.replace('PMLAT',str(latitude))
            pm = pm.replace('STURL','#'+str(style))
            pm = pm.replace('PMALT',str(0))
            pm = pm.replace('PMCOLOR',str(pm_color))
            pm = pm.replace('PMCDATA',str(pm_cdata))
            if p in lstring_flag:
                leg = anc_alt/10
                linestring = str(longitude)+','+str(latitude)+','+str(0)+'\n'
                linestring += str(longitude)+','+str(latitude)+','+str(anc_alt-leg)+'\n'
                linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt-leg)+'\n'
                linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt)+'\n'
            else:
                linestring = get_linestring(latitude,longitude,0,anc_lat,anc_lon,anc_alt)
            pm = pm.replace('PMLINE',str(linestring))


            kml += pm
        kml += '</Folder>\n</Document>\n</kml>'

        self.kml = kml
        self.taxa = len(leafs)
        self.err = err
        self.type = typeX



#Build Leaf Z Attributes
class build_kml_leafZ:
    def __init__(self,tree,coords,mydomain,branch_color,branch_width,node_url,alt_grow,proximity,kml_title):
        tree = tree.replace('\n','')
        tree = tree.strip()

        if tree[-1] == "," or tree[-1] == ";":
            tree = tree[0:-1]

        err = False
        typeX = ""

        if tree.count('(') != tree.count(')'):
            err = True
            typeX += 'Your tree contains '+str(tree.count('('))+' open parenthesis "(" and '+str(tree.count(')'))+' close parenthesis ")" '+"\n"
            #return "",0,err,typeX

        if not is_rooted(tree):

            err = True
            typeX += "Your tree does not appear to be rooted. We attempted to force a root, but it may not be the same as you intended. \n If you are sure your tree was rooted, this probably didn't change anything.\n"
            tree = "("+tree+")"


        #variables:
        # proximity
        # alt_grow
        # internal_icon
        # default_color

        internal_icon = str(node_url)

        default_color = str(branch_color)

        alt_grow = int(alt_grow)

        #this sets the number of decimals to round coordinates to when
        #looking for points sharing the same location
        proximity = int(proximity)
        #set the radius size of the circle to scatter them around
        offset = (1*10**(-1*proximity))*.75

        coords = coords.strip()
        tree = tree.strip()

        coords = coords.split('\n')
        lat = {}
        lon = {}
        #track unique coords in order to implement scatter of those overlapping
        uniques = {}
        tstamps = False
        maxtime = datetime.datetime.min

        icons = {}
        for line in coords:
            if line != '':
                curr = line.split(';')
                if 3 <= len(curr):
                    lat[curr[0]] = float(curr[1].strip())
                    lon[curr[0]] = float(curr[2].strip())

                    title = str(round(float(curr[1]),proximity))+'_'+str(round(float(curr[2]),proximity))
                    n = 0
                    if title in uniques:
                        n = int(uniques[title])
                    uniques[title] = n + 1


                    if 4 <= len(curr):
                        if curr[3].strip() == '':
                            icons[curr[0]] = 'default'
                        else:
                            icons[curr[0]] = curr[3].strip()


                        #if datetime set in CSV, extract and store in dictionary
                        if 5 <= len(curr):
                            #date
                            #format= year-mm-day:hour:
                            if tstamps == False:
                                tstamps = {}
                            if len(str(curr[4].strip())) != 0:
                                curdate = curr[4].strip().split('-')
                                yr = int(curdate[0])
                                tmp_date = datetime.datetime(yr,01,01)
                                if 2 <= len(curdate):
                                    mn = int(curdate[1])
                                    tmp_date = tmp_date.replace(month = mn)
                                    if 3 <= len(curdate):
                                        daytime = curdate[2].split('T')
                                        dy = int(daytime[0])
                                        tmp_date = tmp_date.replace(day = dy)
                                        if 2 <= len(daytime):
                                            daytime = daytime[1].split(':')
                                            hr = int(daytime[0])
                                            tmp_date = tmp_date.replace(hour = hr)
                                            if 2 <= len(daytime):
                                                mt = int(daytime[1])
                                                tmp_date = tmp_date.replace(minute = mt)
                                                if 3 <= len(daytime):
                                                    sc = int(daytime[2])
                                                    tmp_date = tmp_date.replace(second = sc)
                                tstamps[curr[0]] = tmp_date
                                if maxtime < tmp_date:
                                    maxtime = tmp_date

                    else:
                        icons[curr[0]] = 'default'

        used_uniques = {}
        for i,t in uniques.items():
            if 1< int(t):
                used_uniques[i] = 0


        kml = tree
        leafs = [1,2,3,4]


        ancestor = ""
        cur_anc = 0
        leafs = {}
        nodes = {}
        rank = {}
        nodes[0]="root"
        cur_leaf = ""
        isleaf = False
        pos = 0
        c = tree[pos]
        depth = 0
        comma = 0
        maxdepth = 0
        rank = {}
        rank[cur_anc] = 0
        children = {}
        children[cur_anc] = []


        for pos in range(0,len(tree)):
            c = tree[pos]
            if c == '(':
                if isleaf and 0<len(cur_leaf):
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth += 1
                if maxdepth < depth:
                    maxdepth = depth
                last_anc = cur_anc
                cur_anc = 'HTU_'+str(len(nodes))
                children[cur_anc] = []
                nodes[cur_anc] = last_anc
                rank[cur_anc] = depth
                children[last_anc].append(cur_anc)
                isleaf=True
            elif c == ')':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth -= 1
                cur_anc = nodes[cur_anc]
                isleaf=False
            elif c == ',':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    rank[cur_leaf] = depth
                    leafs[cur_leaf] = cur_anc
                    children[cur_anc].append(cur_leaf)
                cur_leaf = ""
                isleaf = True
            elif c==":":
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                isleaf = False
                cur_leaf = ""
            elif isleaf:
                cur_leaf += c
                cur_leaf = cur_leaf.lstrip()

        if len(lat)<len(leafs) or len(lon)<len(leafs):
            err = True
            typeX += 'There seems to be something missing.'+str(len(leafs))+' tips existed in your tree and '+str(len(lat))+' lat and '+str(len(lon))+" lon existed\n"

        #this function scatters any points of shared radius = 'offset'
        #around a circle at equal distances
        #if timestamps were given, it also fills any black timestamps with the maxtime value
        for nm,anc in leafs.items():
            if tstamps != False:
                if nm not in tstamps:
                    tstamps[nm] = maxtime
            try:
                curla = float(lat[nm])
                curlo = float(lon[nm])
            except:
                err = True
                curlo = lon.items()[-1][1]
                curla = lat.items()[-1][1]
                typeX += "Not all leaf-nodes in your tree are found in your coordinates file. See, "+str(nm)+". For now we tried to just place this node at "+str(curla)+","+str(curlo)+". You'll have to go back and fix it\n"
                lat[nm] = curla
                lon[nm] = curlo

                #return "",0,error,typeX
            title = str(round(float(curla),proximity))+'_'+str(round(float(curlo),proximity))
            if title in used_uniques:
                total = uniques[title]
                used = int(used_uniques[title])

                #scatter points sharing lat/lon around a circle of radius = 'offset'

                angle = float(360)/(total)
                angle = radians(angle*used)
                tmpx = cos(angle) * offset
                tmpy = sin(angle) * offset
                tmpx += -offset
                tmpy += -offset
                tmp_lon = curlo + tmpx
                tmp_lat = curla + tmpy

                if tmp_lon < -180:
                    tmp_lon += 360
                elif 180 < tmp_lon:
                    tmp_lon += -360

                #still testing the scatter feature
                lat[nm] = round(float(tmp_lat),proximity)
                lon[nm] = round(float(tmp_lon),proximity)

                used_uniques[title] = used+1



        #rank = sorted(rank.items(),reverse=True)
        rankorder = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        lstring_flag = [] #used to later deterime if a branch is a rectangular cladogram
        altitude = {}

        for n,a in leafs.items():
            altitude[n] = 0


        #set the altitude,lat,lon for each internal node
        for n in rankorder:
            r = n[1]
            n = n[0]
            try:
                a = leafs[n]
                altitude[n] = 0.0
            except:
                child_list = children[n]
                max_alt = 0
                min_time = datetime.datetime.today()
                max_dist = 0
                child_count = len(child_list)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                ct = 0
                last_c = ""
                tot_lon = 0
                tot_lat = 0
                for c in child_list:
                    alt = altitude[c]
                    if max_alt<alt:
                        max_alt = alt
                    if tstamps != False:
                        if tstamps[c]<min_time:
                            min_time = tstamps[c]
                    curlat = float(lat[c])
                    curlon = float(lon[c])
                    if max_lat<curlat:
                        max_lat = curlat
                    if max_lon<curlon:
                        max_lon = curlon
                    if curlat<min_lat:
                        min_lat = curlat
                    if curlon<min_lon:
                        min_lon = curlon
                    tot_lon += curlon
                    tot_lat += curlat
                    ct+=1
                    last_c = c

                curlat = tot_lat/ct
                curlon = tot_lon/ct
                if curlon<-180:
                    curlon += 360
                if 180<curlon:
                    curlon -= 360
                """
                lat[n] = (max_lat + min_lat)/2
                lon[n] = get_lon_midpoint(max_lon,min_lon)
                lonvalue = min((max_lon-min_lon),(min_lon-(max_lon-360)))
                dist = sqrt(((lonvalue)**2) + ((max_lat-min_lat)**2))
                """
                lat[n] = float(curlat)
                lon[n] = float(curlon)
                max_dist = 0
                for c in child_list:
                    m1 = float(lon[n])
                    m2 = float(lon[c])
                    v = max(m1,m2)-min(m1,m2)
                    if v < -180:
                        v += 360
                    elif 180 < v:
                        v -=360
                    dist = sqrt(((v)**2) + ((lat[n]-lat[c])**2))
                    if dist <= 10.0:
                        lstring_flag.append(c)

                    if max_dist<dist:
                        max_dist = dist

                dist = max_dist
                if tstamps != False:
                    tstamps[n] = min_time

                new_alt = max_alt + (alt_grow * dist * .5) + alt_grow

                altitude[n] = int(new_alt)




        kml = '<?xml version="1.0" encoding="UTF-8"?>\n <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n <Document>\n\t <name>&title</name>\n\t <open>1</open>\n\t <Snippet maxLines="2"></Snippet>\n'
        if err:
            kml += "\n<description><![CDATA[\n"
            kml += typeX
            kml += "\n]]></description>"
            kml = kml.replace('&title',"ERRORS")
        else:
            kml = kml.replace('&title',kml_title)

        highlight_branch_width = str(branch_width*2)
        branch_width = str(branch_width)
        style =  '\t<Style id="ICNUMa">\n' \
        '            <IconStyle>\n' \
        '                <scale>.25</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '                <scale>0</scale>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '        </Style>\n' \
        '        <Style id="ICNUMb">\n' \
        '            <IconStyle>\n' \
        '                <scale>.95</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+highlight_branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '            </Style>\n' \
        '         <StyleMap id="ICNUM">\n' \
        '            <Pair>\n' \
        '                <key>normal</key>\n' \
        '                <styleUrl>#ICNUMa</styleUrl>\n' \
        '            </Pair>\n' \
        '              <Pair>\n' \
        '                   <key>highlight</key>\n' \
        '                   <styleUrl>#ICNUMb</styleUrl>\n' \
        '              </Pair>\n' \
        '         </StyleMap>\n'


        kml += style.replace('ICURL',internal_icon).replace('ICNUM',str(0))

        used = {}
        used['default'] = 0
        styles = {}
        ct = 1
        for name,icon in icons.items():
            if icon in used:
                styles[name] = used[icon]
            else:
                kml += style.replace('ICURL',icon).replace('ICNUM',str(ct))
                styles[name] = ct
                used[icon] = ct
                ct+=1

        kml += '<Folder>\n <name>Leaf Z</name>\n <open>0</open>\n'


        placemark = '<Placemark>\n' \
        '        <name>PMNAME</name>\n' \
        '        PMTIMESTAMP' \
        '        <description><![CDATA[PMCDATA]]></description>\n' \
        '        <Snippet maxLines="2"></Snippet>\n' \
        '        <styleUrl>STURL</styleUrl>\n' \
        '        <LineString>\n' \
        '            <extrude>0</extrude>\n' \
        '            <tessellate>0</tessellate>\n' \
        '            <altitudeMode>relativeToGround</altitudeMode>\n' \
        '            <coordinates>PMLINE</coordinates>\n' \
        '        </LineString>\n' \
        '    </Placemark>\n'
        timestamp = '<TimeStamp><when>pmtstamp</when></TimeStamp>'

        for p,anc in leafs.items():
            latitude = float(lat[p])
            longitude = float(lon[p])
            anc_lat = float(lat[anc])
            anc_lon = float(lon[anc])
            anc_alt = int(float(altitude[anc]))
            pm_color = default_color

            pm_cdata = '<body>'
            #build description window
            ahref = '<b>Ancestor: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(anc_lon)+'&lat='+str(anc_lat)+'&alt='+str(anc_alt)+'">'+str(anc)+'</a><br>'
            pm_cdata += ahref

            pm_cdata += '</body>'

            try:
                style = styles[p]
            except:
                style = styles.items()[-1][1]

            tstring = ''
            if tstamps != False:
                if p in tstamps:
                    ts = tstamps[p]
                    ts = ts.isoformat()
                    tstring = timestamp.replace('pmtstamp',str(ts))

            pm = placemark.replace('PMNAME',str(p))
            pm = pm.replace('PMTIMESTAMP',tstring)
            pm = pm.replace('PMLON',str(longitude))
            pm = pm.replace('PMLAT',str(latitude))
            pm = pm.replace('STURL','#'+str(style))
            pm = pm.replace('PMALT',str(0))
            pm = pm.replace('PMCOLOR',str(pm_color))
            pm = pm.replace('PMCDATA',str(pm_cdata))
            if p in lstring_flag:
                leg = anc_alt/10
                linestring = str(longitude)+','+str(latitude)+','+str(0)+'\n'
                linestring += str(longitude)+','+str(latitude)+','+str(anc_alt-leg)+'\n'
                linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt-leg)+'\n'
                linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt)+'\n'
            else:
                linestring = get_linestring(latitude,longitude,0,anc_lat,anc_lon,anc_alt)
            pm = pm.replace('PMLINE',str(linestring))


            kml += pm
        kml += '</Folder>\n</Document>\n</kml>'

        self.kml = kml
        self.taxa = len(leafs)
        self.err = err
        self.type = typeX



#Build Tree Nodes
class build_kml_treenodes:
    def __init__(self,tree,coords,mydomain,branch_color,branch_width,node_url,alt_grow,proximity,kml_title):
        tree = tree.replace('\n','')
        tree = tree.strip()

        if tree[-1] == "," or tree[-1] == ";":
            tree = tree[0:-1]

        err = False
        typeX = ""

        if tree.count('(') != tree.count(')'):
            err = True
            typeX += 'Your tree contains '+str(tree.count('('))+' open parenthesis "(" and '+str(tree.count(')'))+' close parenthesis ")" '+"\n"
            #return "",0,err,typeX

        if not is_rooted(tree):

            err = True
            typeX += "Your tree does not appear to be rooted. We attempted to force a root, but it may not be the same as you intended. \n If you are sure your tree was rooted, this probably didn't change anything.\n"
            tree = "("+tree+")"


        #variables:
        # proximity
        # alt_grow
        # internal_icon
        # default_color

        internal_icon = str(node_url)

        default_color = str(branch_color)

        alt_grow = int(alt_grow)

        #this sets the number of decimals to round coordinates to when
        #looking for points sharing the same location
        proximity = int(proximity)
        #set the radius size of the circle to scatter them around
        offset = (1*10**(-1*proximity))*.75

        coords = coords.strip()
        tree = tree.strip()

        coords = coords.split('\n')
        lat = {}
        lon = {}
        #track unique coords in order to implement scatter of those overlapping
        uniques = {}
        tstamps = False
        maxtime = datetime.datetime.min

        icons = {}
        for line in coords:
            if line != '':
                curr = line.split(';')
                if 3 <= len(curr):
                    lat[curr[0]] = float(curr[1].strip())
                    lon[curr[0]] = float(curr[2].strip())

                    title = str(round(float(curr[1]),proximity))+'_'+str(round(float(curr[2]),proximity))
                    n = 0
                    if title in uniques:
                        n = int(uniques[title])
                    uniques[title] = n + 1


                    if 4 <= len(curr):
                        if curr[3].strip() == '':
                            icons[curr[0]] = 'default'
                        else:
                            icons[curr[0]] = curr[3].strip()


                        #if datetime set in CSV, extract and store in dictionary
                        if 5 <= len(curr):
                            #date
                            #format= year-mm-day:hour:
                            if tstamps == False:
                                tstamps = {}
                            if len(str(curr[4].strip())) != 0:
                                curdate = curr[4].strip().split('-')
                                yr = int(curdate[0])
                                tmp_date = datetime.datetime(yr,01,01)
                                if 2 <= len(curdate):
                                    mn = int(curdate[1])
                                    tmp_date = tmp_date.replace(month = mn)
                                    if 3 <= len(curdate):
                                        daytime = curdate[2].split('T')
                                        dy = int(daytime[0])
                                        tmp_date = tmp_date.replace(day = dy)
                                        if 2 <= len(daytime):
                                            daytime = daytime[1].split(':')
                                            hr = int(daytime[0])
                                            tmp_date = tmp_date.replace(hour = hr)
                                            if 2 <= len(daytime):
                                                mt = int(daytime[1])
                                                tmp_date = tmp_date.replace(minute = mt)
                                                if 3 <= len(daytime):
                                                    sc = int(daytime[2])
                                                    tmp_date = tmp_date.replace(second = sc)
                                tstamps[curr[0]] = tmp_date
                                if maxtime < tmp_date:
                                    maxtime = tmp_date

                    else:
                        icons[curr[0]] = 'default'

        used_uniques = {}
        for i,t in uniques.items():
            if 1< int(t):
                used_uniques[i] = 0


        kml = tree
        leafs = [1,2,3,4]


        ancestor = ""
        cur_anc = 0
        leafs = {}
        nodes = {}
        rank = {}
        nodes[0]="root"
        cur_leaf = ""
        isleaf = False
        pos = 0
        c = tree[pos]
        depth = 0
        comma = 0
        maxdepth = 0
        rank = {}
        rank[cur_anc] = 0
        children = {}
        children[cur_anc] = []


        for pos in range(0,len(tree)):
            c = tree[pos]
            if c == '(':
                if isleaf and 0<len(cur_leaf):
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth += 1
                if maxdepth < depth:
                    maxdepth = depth
                last_anc = cur_anc
                cur_anc = 'HTU_'+str(len(nodes))
                children[cur_anc] = []
                nodes[cur_anc] = last_anc
                rank[cur_anc] = depth
                children[last_anc].append(cur_anc)
                isleaf=True
            elif c == ')':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth -= 1
                cur_anc = nodes[cur_anc]
                isleaf=False
            elif c == ',':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    rank[cur_leaf] = depth
                    leafs[cur_leaf] = cur_anc
                    children[cur_anc].append(cur_leaf)
                cur_leaf = ""
                isleaf = True
            elif c==":":
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                isleaf = False
                cur_leaf = ""
            elif isleaf:
                cur_leaf += c
                cur_leaf = cur_leaf.lstrip()

        if len(lat)<len(leafs) or len(lon)<len(leafs):
            err = True
            typeX += 'There seems to be something missing.'+str(len(leafs))+' tips existed in your tree and '+str(len(lat))+' lat and '+str(len(lon))+" lon existed\n"

        #this function scatters any points of shared radius = 'offset'
        #around a circle at equal distances
        #if timestamps were given, it also fills any black timestamps with the maxtime value
        for nm,anc in leafs.items():
            if tstamps != False:
                if nm not in tstamps:
                    tstamps[nm] = maxtime
            try:
                curla = float(lat[nm])
                curlo = float(lon[nm])
            except:
                err = True
                curlo = lon.items()[-1][1]
                curla = lat.items()[-1][1]
                typeX += "Not all leaf-nodes in your tree are found in your coordinates file. See, "+str(nm)+". For now we tried to just place this node at "+str(curla)+","+str(curlo)+". You'll have to go back and fix it\n"
                lat[nm] = curla
                lon[nm] = curlo

                #return "",0,error,typeX
            title = str(round(float(curla),proximity))+'_'+str(round(float(curlo),proximity))
            if title in used_uniques:
                total = uniques[title]
                used = int(used_uniques[title])

                #scatter points sharing lat/lon around a circle of radius = 'offset'

                angle = float(360)/(total)
                angle = radians(angle*used)
                tmpx = cos(angle) * offset
                tmpy = sin(angle) * offset
                tmpx += -offset
                tmpy += -offset
                tmp_lon = curlo + tmpx
                tmp_lat = curla + tmpy

                if tmp_lon < -180:
                    tmp_lon += 360
                elif 180 < tmp_lon:
                    tmp_lon += -360

                #still testing the scatter feature
                lat[nm] = round(float(tmp_lat),proximity)
                lon[nm] = round(float(tmp_lon),proximity)

                used_uniques[title] = used+1



        #rank = sorted(rank.items(),reverse=True)
        rankorder = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        lstring_flag = [] #used to later deterime if a branch is a rectangular cladogram
        altitude = {}

        for n,a in leafs.items():
            altitude[n] = 0


        #set the altitude,lat,lon for each internal node
        for n in rankorder:
            r = n[1]
            n = n[0]
            try:
                a = leafs[n]
                altitude[n] = 0.0
            except:
                child_list = children[n]
                max_alt = 0
                min_time = datetime.datetime.today()
                max_dist = 0
                child_count = len(child_list)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                ct = 0
                last_c = ""
                tot_lon = 0
                tot_lat = 0
                for c in child_list:
                    alt = altitude[c]
                    if max_alt<alt:
                        max_alt = alt
                    if tstamps != False:
                        if tstamps[c]<min_time:
                            min_time = tstamps[c]
                    curlat = float(lat[c])
                    curlon = float(lon[c])
                    if max_lat<curlat:
                        max_lat = curlat
                    if max_lon<curlon:
                        max_lon = curlon
                    if curlat<min_lat:
                        min_lat = curlat
                    if curlon<min_lon:
                        min_lon = curlon
                    tot_lon += curlon
                    tot_lat += curlat
                    ct+=1
                    last_c = c

                curlat = tot_lat/ct
                curlon = tot_lon/ct
                if curlon<-180:
                    curlon += 360
                if 180<curlon:
                    curlon -= 360
                """
                lat[n] = (max_lat + min_lat)/2
                lon[n] = get_lon_midpoint(max_lon,min_lon)
                lonvalue = min((max_lon-min_lon),(min_lon-(max_lon-360)))
                dist = sqrt(((lonvalue)**2) + ((max_lat-min_lat)**2))
                """
                lat[n] = float(curlat)
                lon[n] = float(curlon)
                max_dist = 0
                for c in child_list:
                    m1 = float(lon[n])
                    m2 = float(lon[c])
                    v = max(m1,m2)-min(m1,m2)
                    if v < -180:
                        v += 360
                    elif 180 < v:
                        v -=360
                    dist = sqrt(((v)**2) + ((lat[n]-lat[c])**2))
                    if dist <= 10.0:
                        lstring_flag.append(c)

                    if max_dist<dist:
                        max_dist = dist

                dist = max_dist
                if tstamps != False:
                    tstamps[n] = min_time

                new_alt = max_alt + (alt_grow * dist * .5) + alt_grow

                altitude[n] = int(new_alt)




        kml = '<?xml version="1.0" encoding="UTF-8"?>\n <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n <Document>\n\t <name>&title</name>\n\t <open>1</open>\n\t <Snippet maxLines="2"></Snippet>\n'
        if err:
            kml += "\n<description><![CDATA[\n"
            kml += typeX
            kml += "\n]]></description>"
            kml = kml.replace('&title',"ERRORS")
        else:
            kml = kml.replace('&title',kml_title)

        highlight_branch_width = str(branch_width*2)
        branch_width = str(branch_width)
        style =  '\t<Style id="ICNUMa">\n' \
        '            <IconStyle>\n' \
        '                <scale>.25</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '                <scale>0</scale>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '        </Style>\n' \
        '        <Style id="ICNUMb">\n' \
        '            <IconStyle>\n' \
        '                <scale>.95</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+highlight_branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '            </Style>\n' \
        '         <StyleMap id="ICNUM">\n' \
        '            <Pair>\n' \
        '                <key>normal</key>\n' \
        '                <styleUrl>#ICNUMa</styleUrl>\n' \
        '            </Pair>\n' \
        '              <Pair>\n' \
        '                   <key>highlight</key>\n' \
        '                   <styleUrl>#ICNUMb</styleUrl>\n' \
        '              </Pair>\n' \
        '         </StyleMap>\n'


        kml += style.replace('ICURL',internal_icon).replace('ICNUM',str(0))

        used = {}
        used['default'] = 0
        styles = {}
        ct = 1
        for name,icon in icons.items():
            if icon in used:
                styles[name] = used[icon]
            else:
                kml += style.replace('ICURL',icon).replace('ICNUM',str(ct))
                styles[name] = ct
                used[icon] = ct
                ct+=1


        kml += '<Folder>\n <name>HTU Nodes</name>\n <open>0</open>\n'

        placemark = '<Placemark>\n' \
        '        <name>PMNAME</name>\n' \
        '        PMTIMESTAMP' \
        '        <description><![CDATA[PMCDATA]]></description>\n' \
        '        <Snippet maxLines = "2"></Snippet>\n' \
        '        <styleUrl>STURL</styleUrl>\n' \
        '        <Point id="pt_PMNAME">\n' \
        '            <extrude>0</extrude>\n' \
        '            <altitudeMode>relativeToGround</altitudeMode>\n' \
        '            <coordinates>PMLON,PMLAT,PMALT</coordinates>\n' \
        '        </Point>\n' \
        '    </Placemark>\n'
        timestamp = '<TimeStamp><when>pmtstamp</when></TimeStamp>'


        for p,anc in nodes.items():
            latitude = float(lat[p])
            longitude = float(lon[p])
            alt = float(altitude[p])
            if str(p) != str(0):
                anc_lat = float(lat[anc])
                anc_lon = float(lon[anc])
                anc_alt = float(altitude[anc])
                pm_color = default_color

                pm_cdata = '<body>'
                #build description window
                ahref = '<b>Ancestor: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(anc_lon)+'&lat='+str(anc_lat)+'&alt='+str(int(anc_alt))+'">'+str(anc)+'</a><br>\n'
                pm_cdata += ahref

                child_list = children[p]
                for c in child_list:

                    chld_lat = float(lat[c])
                    chld_lon = float(lon[c])
                    chld_alt = float(altitude[c])
                    ahref = '</br><b>Descendant: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(chld_lon)+'&lat='+str(chld_lat)+'&alt='+str(chld_alt)+'">'+str(c)+'</a><br>\n'
                    pm_cdata += ahref

                pm_cdata += '</body>'

                tstring = ''
                if tstamps != False:
                    if p in tstamps:
                        ts = tstamps[p]
                        ts = ts.isoformat()
                        tstring = timestamp.replace('pmtstamp',str(ts))

                pm = placemark.replace('PMNAME',str(p))
                pm = pm.replace('PMTIMESTAMP',tstring)
                pm = pm.replace('PMLON',str(longitude))
                pm = pm.replace('PMLAT',str(latitude))
                pm = pm.replace('PMALT',str(int(alt)))
                pm = pm.replace('STURL','#'+str(0))
                pm = pm.replace('PMCOLOR',str(pm_color))
                pm = pm.replace('PMCDATA',str(pm_cdata))
                if p in lstring_flag:
                    leg = (anc_alt)/10
                    while (anc_alt - leg) < alt:
                        leg = leg * .5
                    linestring = str(longitude)+','+str(latitude)+','+str(alt)+'\n'
                    linestring += str(longitude)+','+str(latitude)+','+str(anc_alt-leg)+'\n'
                    linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt-leg)+'\n'
                    linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt)+'\n'
                else:
                    linestring = get_linestring(latitude,longitude,alt,anc_lat,anc_lon,anc_alt)

                pm = pm.replace('PMLINE',str(linestring))
                kml += pm
            else:
                pass
        kml += '</Folder>\n</Document>\n</kml>'

        self.kml = kml
        self.taxa = len(leafs)
        self.err = err
        self.type = typeX



#Build Tree Constructs
class build_kml_treenetworks:
    def __init__(self,tree,coords,mydomain,branch_color,branch_width,node_url,alt_grow,proximity,kml_title):
        tree = tree.replace('\n','')
        tree = tree.strip()

        if tree[-1] == "," or tree[-1] == ";":
            tree = tree[0:-1]

        err = False
        typeX = ""

        if tree.count('(') != tree.count(')'):
            err = True
            typeX += 'Your tree contains '+str(tree.count('('))+' open parenthesis "(" and '+str(tree.count(')'))+' close parenthesis ")" '+"\n"
            #return "",0,err,typeX

        if not is_rooted(tree):

            err = True
            typeX += "Your tree does not appear to be rooted. We attempted to force a root, but it may not be the same as you intended. \n If you are sure your tree was rooted, this probably didn't change anything.\n"
            tree = "("+tree+")"


        #variables:
        # proximity
        # alt_grow
        # internal_icon
        # default_color

        internal_icon = str(node_url)

        default_color = str(branch_color)

        alt_grow = int(alt_grow)

        #this sets the number of decimals to round coordinates to when
        #looking for points sharing the same location
        proximity = int(proximity)
        #set the radius size of the circle to scatter them around
        offset = (1*10**(-1*proximity))*.75

        coords = coords.strip()
        tree = tree.strip()

        coords = coords.split('\n')
        lat = {}
        lon = {}
        #track unique coords in order to implement scatter of those overlapping
        uniques = {}
        tstamps = False
        maxtime = datetime.datetime.min

        icons = {}
        for line in coords:
            if line != '':
                curr = line.split(';')
                if 3 <= len(curr):
                    lat[curr[0]] = float(curr[1].strip())
                    lon[curr[0]] = float(curr[2].strip())

                    title = str(round(float(curr[1]),proximity))+'_'+str(round(float(curr[2]),proximity))
                    n = 0
                    if title in uniques:
                        n = int(uniques[title])
                    uniques[title] = n + 1


                    if 4 <= len(curr):
                        if curr[3].strip() == '':
                            icons[curr[0]] = 'default'
                        else:
                            icons[curr[0]] = curr[3].strip()


                        #if datetime set in CSV, extract and store in dictionary
                        if 5 <= len(curr):
                            #date
                            #format= year-mm-day:hour:
                            if tstamps == False:
                                tstamps = {}
                            if len(str(curr[4].strip())) != 0:
                                curdate = curr[4].strip().split('-')
                                yr = int(curdate[0])
                                tmp_date = datetime.datetime(yr,01,01)
                                if 2 <= len(curdate):
                                    mn = int(curdate[1])
                                    tmp_date = tmp_date.replace(month = mn)
                                    if 3 <= len(curdate):
                                        daytime = curdate[2].split('T')
                                        dy = int(daytime[0])
                                        tmp_date = tmp_date.replace(day = dy)
                                        if 2 <= len(daytime):
                                            daytime = daytime[1].split(':')
                                            hr = int(daytime[0])
                                            tmp_date = tmp_date.replace(hour = hr)
                                            if 2 <= len(daytime):
                                                mt = int(daytime[1])
                                                tmp_date = tmp_date.replace(minute = mt)
                                                if 3 <= len(daytime):
                                                    sc = int(daytime[2])
                                                    tmp_date = tmp_date.replace(second = sc)
                                tstamps[curr[0]] = tmp_date
                                if maxtime < tmp_date:
                                    maxtime = tmp_date

                    else:
                        icons[curr[0]] = 'default'

        used_uniques = {}
        for i,t in uniques.items():
            if 1< int(t):
                used_uniques[i] = 0


        kml = tree
        leafs = [1,2,3,4]


        ancestor = ""
        cur_anc = 0
        leafs = {}
        nodes = {}
        rank = {}
        nodes[0]="root"
        cur_leaf = ""
        isleaf = False
        pos = 0
        c = tree[pos]
        depth = 0
        comma = 0
        maxdepth = 0
        rank = {}
        rank[cur_anc] = 0
        children = {}
        children[cur_anc] = []


        for pos in range(0,len(tree)):
            c = tree[pos]
            if c == '(':
                if isleaf and 0<len(cur_leaf):
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth += 1
                if maxdepth < depth:
                    maxdepth = depth
                last_anc = cur_anc
                cur_anc = 'HTU_'+str(len(nodes))
                children[cur_anc] = []
                nodes[cur_anc] = last_anc
                rank[cur_anc] = depth
                children[last_anc].append(cur_anc)
                isleaf=True
            elif c == ')':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth -= 1
                cur_anc = nodes[cur_anc]
                isleaf=False
            elif c == ',':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    rank[cur_leaf] = depth
                    leafs[cur_leaf] = cur_anc
                    children[cur_anc].append(cur_leaf)
                cur_leaf = ""
                isleaf = True
            elif c==":":
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                isleaf = False
                cur_leaf = ""
            elif isleaf:
                cur_leaf += c
                cur_leaf = cur_leaf.lstrip()

        if len(lat)<len(leafs) or len(lon)<len(leafs):
            err = True
            typeX += 'There seems to be something missing.'+str(len(leafs))+' tips existed in your tree and '+str(len(lat))+' lat and '+str(len(lon))+" lon existed\n"

        #this function scatters any points of shared radius = 'offset'
        #around a circle at equal distances
        #if timestamps were given, it also fills any black timestamps with the maxtime value
        for nm,anc in leafs.items():
            if tstamps != False:
                if nm not in tstamps:
                    tstamps[nm] = maxtime
            try:
                curla = float(lat[nm])
                curlo = float(lon[nm])
            except:
                err = True
                curlo = lon.items()[-1][1]
                curla = lat.items()[-1][1]
                typeX += "Not all leaf-nodes in your tree are found in your coordinates file. See, "+str(nm)+". For now we tried to just place this node at "+str(curla)+","+str(curlo)+". You'll have to go back and fix it\n"
                lat[nm] = curla
                lon[nm] = curlo

                #return "",0,error,typeX
            title = str(round(float(curla),proximity))+'_'+str(round(float(curlo),proximity))
            if title in used_uniques:
                total = uniques[title]
                used = int(used_uniques[title])

                #scatter points sharing lat/lon around a circle of radius = 'offset'

                angle = float(360)/(total)
                angle = radians(angle*used)
                tmpx = cos(angle) * offset
                tmpy = sin(angle) * offset
                tmpx += -offset
                tmpy += -offset
                tmp_lon = curlo + tmpx
                tmp_lat = curla + tmpy

                if tmp_lon < -180:
                    tmp_lon += 360
                elif 180 < tmp_lon:
                    tmp_lon += -360

                #still testing the scatter feature
                lat[nm] = round(float(tmp_lat),proximity)
                lon[nm] = round(float(tmp_lon),proximity)

                used_uniques[title] = used+1



        #rank = sorted(rank.items(),reverse=True)
        rankorder = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        lstring_flag = [] #used to later deterime if a branch is a rectangular cladogram
        altitude = {}

        for n,a in leafs.items():
            altitude[n] = 0


        #set the altitude,lat,lon for each internal node
        for n in rankorder:
            r = n[1]
            n = n[0]
            try:
                a = leafs[n]
                altitude[n] = 0.0
            except:
                child_list = children[n]
                max_alt = 0
                min_time = datetime.datetime.today()
                max_dist = 0
                child_count = len(child_list)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                ct = 0
                last_c = ""
                tot_lon = 0
                tot_lat = 0
                for c in child_list:
                    alt = altitude[c]
                    if max_alt<alt:
                        max_alt = alt
                    if tstamps != False:
                        if tstamps[c]<min_time:
                            min_time = tstamps[c]
                    curlat = float(lat[c])
                    curlon = float(lon[c])
                    if max_lat<curlat:
                        max_lat = curlat
                    if max_lon<curlon:
                        max_lon = curlon
                    if curlat<min_lat:
                        min_lat = curlat
                    if curlon<min_lon:
                        min_lon = curlon
                    tot_lon += curlon
                    tot_lat += curlat
                    ct+=1
                    last_c = c

                curlat = tot_lat/ct
                curlon = tot_lon/ct
                if curlon<-180:
                    curlon += 360
                if 180<curlon:
                    curlon -= 360
                """
                lat[n] = (max_lat + min_lat)/2
                lon[n] = get_lon_midpoint(max_lon,min_lon)
                lonvalue = min((max_lon-min_lon),(min_lon-(max_lon-360)))
                dist = sqrt(((lonvalue)**2) + ((max_lat-min_lat)**2))
                """
                lat[n] = float(curlat)
                lon[n] = float(curlon)
                max_dist = 0
                for c in child_list:
                    m1 = float(lon[n])
                    m2 = float(lon[c])
                    v = max(m1,m2)-min(m1,m2)
                    if v < -180:
                        v += 360
                    elif 180 < v:
                        v -=360
                    dist = sqrt(((v)**2) + ((lat[n]-lat[c])**2))
                    if dist <= 10.0:
                        lstring_flag.append(c)

                    if max_dist<dist:
                        max_dist = dist

                dist = max_dist
                if tstamps != False:
                    tstamps[n] = min_time

                new_alt = max_alt + (alt_grow * dist * .5) + alt_grow

                altitude[n] = int(new_alt)




        kml = '<?xml version="1.0" encoding="UTF-8"?>\n <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n <Document>\n\t <name>&title</name>\n\t <open>1</open>\n\t <Snippet maxLines="2"></Snippet>\n'
        if err:
            kml += "\n<description><![CDATA[\n"
            kml += typeX
            kml += "\n]]></description>"
            kml = kml.replace('&title',"ERRORS")
        else:
            kml = kml.replace('&title',kml_title)

        highlight_branch_width = str(branch_width*2)
        branch_width = str(branch_width)
        style =  '\t<Style id="ICNUMa">\n' \
        '            <IconStyle>\n' \
        '                <scale>.25</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '                <scale>0</scale>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '        </Style>\n' \
        '        <Style id="ICNUMb">\n' \
        '            <IconStyle>\n' \
        '                <scale>.95</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+highlight_branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '            </Style>\n' \
        '         <StyleMap id="ICNUM">\n' \
        '            <Pair>\n' \
        '                <key>normal</key>\n' \
        '                <styleUrl>#ICNUMa</styleUrl>\n' \
        '            </Pair>\n' \
        '              <Pair>\n' \
        '                   <key>highlight</key>\n' \
        '                   <styleUrl>#ICNUMb</styleUrl>\n' \
        '              </Pair>\n' \
        '         </StyleMap>\n'


        kml += style.replace('ICURL',internal_icon).replace('ICNUM',str(0))

        used = {}
        used['default'] = 0
        styles = {}
        ct = 1
        for name,icon in icons.items():
            if icon in used:
                styles[name] = used[icon]
            else:
                kml += style.replace('ICURL',icon).replace('ICNUM',str(ct))
                styles[name] = ct
                used[icon] = ct
                ct+=1


        kml += '<Folder>\n <name>Tree Networks</name>\n <open>0</open>\n'

        placemark = '<Placemark>\n' \
        '        <name>PMNAME</name>\n' \
        '        PMTIMESTAMP' \
        '        <description><![CDATA[PMCDATA]]></description>\n' \
        '        <Snippet maxLines="2"></Snippet>\n' \
        '        <styleUrl>STURL</styleUrl>\n' \
        '        <LineString>\n' \
        '            <extrude>0</extrude>\n' \
        '            <tessellate>0</tessellate>\n' \
        '            <altitudeMode>relativeToGround</altitudeMode>\n' \
        '            <coordinates>PMLINE</coordinates>\n' \
        '        </LineString>\n' \
        '    </Placemark>\n'
        timestamp = '<TimeStamp><when>pmtstamp</when></TimeStamp>'


        for p,anc in nodes.items():
            latitude = float(lat[p])
            longitude = float(lon[p])
            alt = float(altitude[p])
            if str(p) != str(0):
                anc_lat = float(lat[anc])
                anc_lon = float(lon[anc])
                anc_alt = float(altitude[anc])
                pm_color = default_color

                pm_cdata = '<body>'
                #build description window
                ahref = '<b>Ancestor: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(anc_lon)+'&lat='+str(anc_lat)+'&alt='+str(int(anc_alt))+'">'+str(anc)+'</a><br>\n'
                pm_cdata += ahref

                child_list = children[p]
                for c in child_list:

                    chld_lat = float(lat[c])
                    chld_lon = float(lon[c])
                    chld_alt = float(altitude[c])
                    ahref = '</br><b>Descendant: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(chld_lon)+'&lat='+str(chld_lat)+'&alt='+str(chld_alt)+'">'+str(c)+'</a><br>\n'
                    pm_cdata += ahref

                pm_cdata += '</body>'

                tstring = ''
                if tstamps != False:
                    if p in tstamps:
                        ts = tstamps[p]
                        ts = ts.isoformat()
                        tstring = timestamp.replace('pmtstamp',str(ts))

                pm = placemark.replace('PMNAME',str(p))
                pm = pm.replace('PMTIMESTAMP',tstring)
                pm = pm.replace('PMLON',str(longitude))
                pm = pm.replace('PMLAT',str(latitude))
                pm = pm.replace('PMALT',str(int(alt)))
                pm = pm.replace('STURL','#'+str(0))
                pm = pm.replace('PMCOLOR',str(pm_color))
                pm = pm.replace('PMCDATA',str(pm_cdata))
                if p in lstring_flag:
                    leg = (anc_alt)/10
                    while (anc_alt - leg) < alt:
                        leg = leg * .5
                    linestring = str(longitude)+','+str(latitude)+','+str(alt)+'\n'
                    linestring += str(longitude)+','+str(latitude)+','+str(anc_alt-leg)+'\n'
                    linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt-leg)+'\n'
                    linestring += str(anc_lon)+','+str(anc_lat)+','+str(anc_alt)+'\n'
                else:
                    linestring = get_linestring(latitude,longitude,alt,anc_lat,anc_lon,anc_alt)

                pm = pm.replace('PMLINE',str(linestring))
                kml += pm
            else:
                pass
        kml += '</Folder>\n</Document>\n</kml>'

        self.kml = kml
        self.taxa = len(leafs)
        self.err = err
        self.type = typeX



#Build Root Point
class build_kml_rootpoint:
    def __init__(self,tree,coords,mydomain,branch_color,branch_width,node_url,alt_grow,proximity,kml_title):
        tree = tree.replace('\n','')
        tree = tree.strip()

        if tree[-1] == "," or tree[-1] == ";":
            tree = tree[0:-1]

        err = False
        typeX = ""

        if tree.count('(') != tree.count(')'):
            err = True
            typeX += 'Your tree contains '+str(tree.count('('))+' open parenthesis "(" and '+str(tree.count(')'))+' close parenthesis ")" '+"\n"
            #return "",0,err,typeX

        if not is_rooted(tree):

            err = True
            typeX += "Your tree does not appear to be rooted. We attempted to force a root, but it may not be the same as you intended. \n If you are sure your tree was rooted, this probably didn't change anything.\n"
            tree = "("+tree+")"


        #variables:
        # proximity
        # alt_grow
        # internal_icon
        # default_color

        internal_icon = str(node_url)

        default_color = str(branch_color)

        alt_grow = int(alt_grow)

        #this sets the number of decimals to round coordinates to when
        #looking for points sharing the same location
        proximity = int(proximity)
        #set the radius size of the circle to scatter them around
        offset = (1*10**(-1*proximity))*.75

        coords = coords.strip()
        tree = tree.strip()

        coords = coords.split('\n')
        lat = {}
        lon = {}
        #track unique coords in order to implement scatter of those overlapping
        uniques = {}
        tstamps = False
        maxtime = datetime.datetime.min

        icons = {}
        for line in coords:
            if line != '':
                curr = line.split(';')
                if 3 <= len(curr):
                    lat[curr[0]] = float(curr[1].strip())
                    lon[curr[0]] = float(curr[2].strip())

                    title = str(round(float(curr[1]),proximity))+'_'+str(round(float(curr[2]),proximity))
                    n = 0
                    if title in uniques:
                        n = int(uniques[title])
                    uniques[title] = n + 1


                    if 4 <= len(curr):
                        if curr[3].strip() == '':
                            icons[curr[0]] = 'default'
                        else:
                            icons[curr[0]] = curr[3].strip()


                        #if datetime set in CSV, extract and store in dictionary
                        if 5 <= len(curr):
                            #date
                            #format= year-mm-day:hour:
                            if tstamps == False:
                                tstamps = {}
                            if len(str(curr[4].strip())) != 0:
                                curdate = curr[4].strip().split('-')
                                yr = int(curdate[0])
                                tmp_date = datetime.datetime(yr,01,01)
                                if 2 <= len(curdate):
                                    mn = int(curdate[1])
                                    tmp_date = tmp_date.replace(month = mn)
                                    if 3 <= len(curdate):
                                        daytime = curdate[2].split('T')
                                        dy = int(daytime[0])
                                        tmp_date = tmp_date.replace(day = dy)
                                        if 2 <= len(daytime):
                                            daytime = daytime[1].split(':')
                                            hr = int(daytime[0])
                                            tmp_date = tmp_date.replace(hour = hr)
                                            if 2 <= len(daytime):
                                                mt = int(daytime[1])
                                                tmp_date = tmp_date.replace(minute = mt)
                                                if 3 <= len(daytime):
                                                    sc = int(daytime[2])
                                                    tmp_date = tmp_date.replace(second = sc)
                                tstamps[curr[0]] = tmp_date
                                if maxtime < tmp_date:
                                    maxtime = tmp_date

                    else:
                        icons[curr[0]] = 'default'

        used_uniques = {}
        for i,t in uniques.items():
            if 1< int(t):
                used_uniques[i] = 0


        kml = tree
        leafs = [1,2,3,4]


        ancestor = ""
        cur_anc = 0
        leafs = {}
        nodes = {}
        rank = {}
        nodes[0]="root"
        cur_leaf = ""
        isleaf = False
        pos = 0
        c = tree[pos]
        depth = 0
        comma = 0
        maxdepth = 0
        rank = {}
        rank[cur_anc] = 0
        children = {}
        children[cur_anc] = []


        for pos in range(0,len(tree)):
            c = tree[pos]
            if c == '(':
                if isleaf and 0<len(cur_leaf):
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth += 1
                if maxdepth < depth:
                    maxdepth = depth
                last_anc = cur_anc
                cur_anc = 'HTU_'+str(len(nodes))
                children[cur_anc] = []
                nodes[cur_anc] = last_anc
                rank[cur_anc] = depth
                children[last_anc].append(cur_anc)
                isleaf=True
            elif c == ')':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                depth -= 1
                cur_anc = nodes[cur_anc]
                isleaf=False
            elif c == ',':
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    rank[cur_leaf] = depth
                    leafs[cur_leaf] = cur_anc
                    children[cur_anc].append(cur_leaf)
                cur_leaf = ""
                isleaf = True
            elif c==":":
                if isleaf and 0<len(cur_leaf):
                    cur_leaf = cur_leaf.strip()
                    leafs[cur_leaf] = cur_anc
                    rank[cur_leaf] = depth
                    children[cur_anc].append(cur_leaf)
                isleaf = False
                cur_leaf = ""
            elif isleaf:
                cur_leaf += c
                cur_leaf = cur_leaf.lstrip()

        if len(lat)<len(leafs) or len(lon)<len(leafs):
            err = True
            typeX += 'There seems to be something missing.'+str(len(leafs))+' tips existed in your tree and '+str(len(lat))+' lat and '+str(len(lon))+" lon existed\n"

        #this function scatters any points of shared radius = 'offset'
        #around a circle at equal distances
        #if timestamps were given, it also fills any black timestamps with the maxtime value
        for nm,anc in leafs.items():
            if tstamps != False:
                if nm not in tstamps:
                    tstamps[nm] = maxtime
            try:
                curla = float(lat[nm])
                curlo = float(lon[nm])
            except:
                err = True
                curlo = lon.items()[-1][1]
                curla = lat.items()[-1][1]
                typeX += "Not all leaf-nodes in your tree are found in your coordinates file. See, "+str(nm)+". For now we tried to just place this node at "+str(curla)+","+str(curlo)+". You'll have to go back and fix it\n"
                lat[nm] = curla
                lon[nm] = curlo

                #return "",0,error,typeX
            title = str(round(float(curla),proximity))+'_'+str(round(float(curlo),proximity))
            if title in used_uniques:
                total = uniques[title]
                used = int(used_uniques[title])

                #scatter points sharing lat/lon around a circle of radius = 'offset'

                angle = float(360)/(total)
                angle = radians(angle*used)
                tmpx = cos(angle) * offset
                tmpy = sin(angle) * offset
                tmpx += -offset
                tmpy += -offset
                tmp_lon = curlo + tmpx
                tmp_lat = curla + tmpy

                if tmp_lon < -180:
                    tmp_lon += 360
                elif 180 < tmp_lon:
                    tmp_lon += -360

                #still testing the scatter feature
                lat[nm] = round(float(tmp_lat),proximity)
                lon[nm] = round(float(tmp_lon),proximity)

                used_uniques[title] = used+1



        #rank = sorted(rank.items(),reverse=True)
        rankorder = sorted(rank.items(), key=lambda x: x[1], reverse=True)
        lstring_flag = [] #used to later deterime if a branch is a rectangular cladogram
        altitude = {}

        for n,a in leafs.items():
            altitude[n] = 0


        #set the altitude,lat,lon for each internal node
        for n in rankorder:
            r = n[1]
            n = n[0]
            try:
                a = leafs[n]
                altitude[n] = 0.0
            except:
                child_list = children[n]
                max_alt = 0
                min_time = datetime.datetime.today()
                max_dist = 0
                child_count = len(child_list)
                max_lat = -180
                min_lat = 180
                max_lon = -180
                min_lon = 180
                ct = 0
                last_c = ""
                tot_lon = 0
                tot_lat = 0
                for c in child_list:
                    alt = altitude[c]
                    if max_alt<alt:
                        max_alt = alt
                    if tstamps != False:
                        if tstamps[c]<min_time:
                            min_time = tstamps[c]
                    curlat = float(lat[c])
                    curlon = float(lon[c])
                    if max_lat<curlat:
                        max_lat = curlat
                    if max_lon<curlon:
                        max_lon = curlon
                    if curlat<min_lat:
                        min_lat = curlat
                    if curlon<min_lon:
                        min_lon = curlon
                    tot_lon += curlon
                    tot_lat += curlat
                    ct+=1
                    last_c = c

                curlat = tot_lat/ct
                curlon = tot_lon/ct
                if curlon<-180:
                    curlon += 360
                if 180<curlon:
                    curlon -= 360
                """
                lat[n] = (max_lat + min_lat)/2
                lon[n] = get_lon_midpoint(max_lon,min_lon)
                lonvalue = min((max_lon-min_lon),(min_lon-(max_lon-360)))
                dist = sqrt(((lonvalue)**2) + ((max_lat-min_lat)**2))
                """
                lat[n] = float(curlat)
                lon[n] = float(curlon)
                max_dist = 0
                for c in child_list:
                    m1 = float(lon[n])
                    m2 = float(lon[c])
                    v = max(m1,m2)-min(m1,m2)
                    if v < -180:
                        v += 360
                    elif 180 < v:
                        v -=360
                    dist = sqrt(((v)**2) + ((lat[n]-lat[c])**2))
                    if dist <= 10.0:
                        lstring_flag.append(c)

                    if max_dist<dist:
                        max_dist = dist

                dist = max_dist
                if tstamps != False:
                    tstamps[n] = min_time

                new_alt = max_alt + (alt_grow * dist * .5) + alt_grow

                altitude[n] = int(new_alt)




        kml = '<?xml version="1.0" encoding="UTF-8"?>\n <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n <Document>\n\t <name>&title</name>\n\t <open>1</open>\n\t <Snippet maxLines="2"></Snippet>\n'
        if err:
            kml += "\n<description><![CDATA[\n"
            kml += typeX
            kml += "\n]]></description>"
            kml = kml.replace('&title',"ERRORS")
        else:
            kml = kml.replace('&title',kml_title)

        highlight_branch_width = str(branch_width*2)
        branch_width = str(branch_width)
        style =  '\t<Style id="ICNUMa">\n' \
        '            <IconStyle>\n' \
        '                <scale>.25</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '                <scale>0</scale>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '        </Style>\n' \
        '        <Style id="ICNUMb">\n' \
        '            <IconStyle>\n' \
        '                <scale>.95</scale>\n' \
        '                <Icon>\n' \
        '                    <href>ICURL</href>\n' \
        '                </Icon>\n' \
        '            </IconStyle>\n' \
        '            <LabelStyle>\n' \
        '            </LabelStyle>\n' \
        '            <LineStyle>\n' \
        '                <width>'+highlight_branch_width+'</width>\n' \
        '            </LineStyle>\n' \
        '            </Style>\n' \
        '         <StyleMap id="ICNUM">\n' \
        '            <Pair>\n' \
        '                <key>normal</key>\n' \
        '                <styleUrl>#ICNUMa</styleUrl>\n' \
        '            </Pair>\n' \
        '              <Pair>\n' \
        '                   <key>highlight</key>\n' \
        '                   <styleUrl>#ICNUMb</styleUrl>\n' \
        '              </Pair>\n' \
        '         </StyleMap>\n'


        kml += style.replace('ICURL',internal_icon).replace('ICNUM',str(0))

        used = {}
        used['default'] = 0
        styles = {}
        ct = 1
        for name,icon in icons.items():
            if icon in used:
                styles[name] = used[icon]
            else:
                kml += style.replace('ICURL',icon).replace('ICNUM',str(ct))
                styles[name] = ct
                used[icon] = ct
                ct+=1


        kml += '<Folder>\n <name>Tree Networks</name>\n <open>0</open>\n'

        placemark = '<Placemark>\n' \
        '        <name>PMNAME</name>\n' \
        '        PMTIMESTAMP' \
        '        <description><![CDATA[PMCDATA]]></description>\n' \
        '        <Snippet maxLines="2"></Snippet>\n' \
        '        <styleUrl>STURL</styleUrl>\n' \
        '        <LineString>\n' \
        '            <extrude>0</extrude>\n' \
        '            <tessellate>0</tessellate>\n' \
        '            <altitudeMode>relativeToGround</altitudeMode>\n' \
        '            <coordinates>PMLINE</coordinates>\n' \
        '        </LineString>\n' \
        '    </Placemark>\n'
        timestamp = '<TimeStamp><when>pmtstamp</when></TimeStamp>'


        for p,anc in nodes.items():
            latitude = float(lat[p])
            longitude = float(lon[p])
            alt = float(altitude[p])
            if str(p) != str(0):
                pass
            else:
                pm = '  <Placemark>\n' \
                '        <name>Root HTU</name>\n' \
                '        <description><![CDATA[PMCDATA]]></description>\n' \
                '        <styleUrl>#0</styleUrl>\n' \
                '        <Point id="pt_PMNAME">\n' \
                '            <extrude>0</extrude>\n' \
                '            <altitudeMode>relativeToGround</altitudeMode>\n' \
                '            <coordinates>PMLON,PMLAT,PMALT</coordinates>\n' \
                '        </Point>\n' \
                '    </Placemark>\n'
                pm_color = default_color

                pm_cdata = '<body>'

                child_list = children[p]
                for c in child_list:

                    chld_lat = float(lat[c])
                    chld_lon = float(lon[c])
                    chld_alt = float(altitude[c])
                    ahref = '<b>Descendant: </b><a href="'+str(mydomain)+'/flyto.kml?lon='+str(chld_lon)+'&lat='+str(chld_lat)+'&alt='+str(chld_alt)+'">'+str(c)+'</a><br>\n'
                    pm_cdata += ahref


                pm_cdata += '</body>'

                pm = pm.replace('PMNAME',str(p))
                pm = pm.replace('PMLON',str(longitude))
                pm = pm.replace('PMLAT',str(latitude))
                pm = pm.replace('PMALT',str(alt))
                pm = pm.replace('PMCOLOR',str(pm_color))
                pm = pm.replace('PMCDATA',str(pm_cdata))


                tstring = ''
                if tstamps != False:
                    if p in tstamps:
                        ts = tstamps[p]
                        ts = ts.isoformat()
                        tstring = timestamp.replace('pmtstamp',str(ts))
                pm = pm.replace('PMTIMESTAMP',tstring)


            kml += pm
        kml += '</Folder>\n</Document>\n</kml>'

        self.kml = kml
        self.taxa = len(leafs)
        self.err = err
        self.type = typeX

