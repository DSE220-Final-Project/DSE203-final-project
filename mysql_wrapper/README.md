Usage:

```
  wrapper = MysqlWrapper()
  dl_query = "DB1(s1) :- gtd(_, 2013, 12, _, _, _, _, _,'Iraq', _, _, _, _, _, _, _, _, _, s1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _)"
  print dl_query
  print ""
  dataframe = wrapper.execute(dl_query)
````

Output:

```
DB1(s1) :- gtd(_, 2013, 12, _, _, _, _, _,'Iraq', _, _, _, _, _, _, _, _, _, s1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _)

SELECT summary AS s1 FROM  gtd WHERE imonth = 12 AND country_txt = 'Iraq' AND iyear = 2013

{u's1': u'12/01/2013: A suicide bomber detonated an explosive device at the funeral of Mudher Al-Shallal Al-Araki in Muqdadiyah city, Diyala governorate, Iraq. Araki was killed in a roadside bombing the day before. In addition to the assailant, the blast killed at least ten people and injured 25 others. No group claimed responsibility for the attack.'}
{u's1': u'12/01/2013: An explosive device targeted a police patrol in the Al-Nasr wa Al-Salam village, Al-Anbar governorate, Iraq. The blast killed two police officers and injured three others. No group claimed responsibility for the attack.'}
{u's1': u'12/01/2013: An explosive device detonated near a civilian vehicle in Wanah area, Nineveh governorate, Iraq. The blast killed two people and injured one person. No group claimed responsibility for the attack.'}
{u's1': u'12/01/2013: An explosive device targeted the convoy of Arshad Al-Salehi in the Tazah area of Kirkuk, Iraq. Al-Salehi, the chairman of the Turkmen Front and Member of Parliament, was not injured in the blast. No group claimed responsibility for the attack.'}
{u's1': u'12/01/2013: Gunmen opened fire on a police patrol in Al-Riyad district, Kirkuk, Iraq. The shooting killed two officers and injured one other officer. No group claimed responsibility for the attack.'}
{u's1': u'12/01/2013: Assailants abducted the father of Ahmed Nasir Al-Karboli along with five other people from Qaim city, Al-Anbar governorate, Iraq. Al-Karboli is the Iraqi Industry and Minerals Minister. The outcome of the kidnapping is unknown. No group claimed responsibility for the incident.'}
{u's1': u'12/01/2013: Assailants shot and killed a soldier in front of the Al-Nida Mosque north of Baghdad city, Baghdad governorate, Iraq. No group claimed responsibility for the attack.'}
....
.
.
````