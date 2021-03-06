// hive query generate top sections' id:name mapping
// select s.id, s.section_name from 
//  ( select id, section_name from cdw.dim_section_complete where load_time = '201702220000' ) s 
//  join 
//  (select section_id, sum(revenue_in_usd) as revenue_in_usd from mx3.supply_preagg_daily_orc 
//    where datestamp >= '20170201' and datestamp <= '20170222' 
//    group by section_id order by revenue_in_usd desc limit 1000 ) p 
//   on s.id = p.section_id 
var topsections = {
    4115128:'attcobrandmediastrm',
    4250754:'hpstrm',
    4402687:'newsstrm',
    4421334:'newsministrm',
    4492584:'sportsstrm',
    4492766:'sportsministrm',
    4492794:'financestrm',
    4494903:'hmrnstrm',
    4511656:'mystrm',
    4871337:'mailandroidappstrm',
    4893923:'mailodinstrm (basic mail)',
    4923806:'frontiermailstrm',
    4923815:'verizonmailstrm',
    4923847:'postcardmailinboxstrm',
    4923850:'postcardmailmessagestrm',
    4964125:'attmailbasicstrm',
    4964393:'sportsnativestrm',
    5000003:'answersmobilestrm',
    5192354:'tumblrstrm',
    5317864:'mailiosappstrm',
    5324856:'mailandroidliststrm',
    5324857:'mailandroidmessagestrm',
    5324858:'mailiosliststrm',
    5324859:'mailiosmessagestrm',
    5354120:'tumblrmobilestrm',
    5381074:'attsbcportalstrm',
    5413222:'mailleftrailstrm',
    5413223:'techmagazinestrm',
    5413226:'DEhomepagestrm',
    5413227:'UKhomepagestrm',
    5413228:'FRhomepagestrm',
    5413229:'IThomepagestrm',
    5413230:'EShomepagestrm',
    5413231:'BRhomepagestrm',
    5413232:'INhomepagestrm',
    5413235:'SGhomepagestrm',
    5413237:'TWhomepagestrm',
    5413238:'HKhomepagestrm',
    5413241:'CAhomepagestrm',
    5413242:'US-EShomepagestrm',
    5413244:'IDhomepagestrm',
    5413256:'DEhomeruntabletstrm',
    5413257:'UKhomeruntabletstrm',
    5413258:'FRhomeruntabletstrm',
    5413266:'AUhomeruntabletstrm',
    5413267:'TWhomepagearticlestrm',
    5413268:'HKhomepagearticlestrm',
    5413271:'CAhomeruntabletstrm',
    5413286:'DEhomerunmobilestrm',
    5413287:'UKhomerunmobilestrm',
    5413288:'FRhomerunmobilestrm',
    5413289:'IThomerunmobilestrm',
    5413291:'BRhomerunmobilestrm',
    5413292:'INhomerunmobilestrm',
    5413295:'SGhomerunmobilestrm',
    5413296:'AUhomerunmobilestrm',
    5413301:'CAhomerunmobilestrm',
    5413302:'US-EShomerunmobilestrm',
    5413350:'ESmailpcstrm',
    5413351:'BRmailpcstrm',
    5413352:'INmailpcstrm',
    5413353:'PHmailpcstrm',
    5413354:'MYmailpcstrm',
    5413355:'SGmailpcstrm',
    5413356:'AUmailpcstrm',
    5413357:'TWmailpcstrm',
    5413358:'HKmailpcstrm',
    5413359:'XE_XAmailpcstrm',
    5413360:'MXmailpcstrm',
    5413361:'CAmailpcstrm',
    5413363:'ARmailpcstrm',
    5413364:'IDmailpcstrm',
    5413365:'VNmailpcstrm',
    5413371:'ROmailpcstrm',
    5413373:'SEmailpcstrm',
    5413374:'GRmailpcstrm',
    5413436:'DEmailandroidliststrm',
    5413437:'UKmailandroidliststrm',
    5413438:'FRmailandroidliststrm',
    5413441:'BRmailandroidliststrm',
    5413442:'INmailandroidliststrm',
    5413445:'SGmailandroidliststrm',
    5413446:'AUmailandroidliststrm',
    5413447:'TWmailandroidliststrm',
    5413451:'CAmailandroidliststrm',
    5413467:'UKmailiosliststrm',
    5413497:'UKmailandroidmessagestrm',
    5413498:'FRmailandroidmessagestrm',
    5413501:'BRmailandroidmessagestrm',
    5413506:'AUmailandroidmessagestrm',
    5413511:'CAmailandroidmessagestrm',
    5413628:'moviesmagazinestrm',
    5413638:'CArogershpstrm',
    5413647:'attmyyahoostrm',
    5413657:'answersdesktopstrm',
    5413696:'homerununifiedappiosstrm',
    5413705:'fantasyandroidappstrm',
    5413706:'fantasyiosappstrm',
    5413718:'hmrnandroidstrm',
    5413719:'sportsnativeandroidstrm',
    5413723:'homerununifiedappandroidstrm',
    5413782:'sportsnative_doubleplay_strm_ios',
    5413785:'sportsnative_doubleplay_strm_android',
    5413786:'financenativestrm_doubleplay_ios',
    5413797:'TWhomerunmobileandroidstrm',
    5413798:'HKhomerunmobileandroidstrm',
    5413800:'attmailmessageliststrm',
    5413806:'NZhomepagestrm',
    5413811:'NZmailstrm',
    5413994:'yahoo_appleww_us_web_apple_curve_mobile',
    5414164:'yahoo_frontpage_us_web_apple_curve_mobile',
    5414993:'yahoo_mobile_us_web_curve_mobile',
    5415009:'yahoo_mobile_us_web_apple_curve_mobile',
    5415734:'yahoo_apple_ipad_trans_intl_curve_tablet',
    5415742:'yahoo_apple_ipad_trans_us_curve_tablet',
    5416434:'yahoo_tablet_us_web_yfp-hrtab-900_curve_tablet',
    5417079:'UKmailinboxstrm',
    5417080:'UKmailleftrailstrm',
    5417084:'DEmailinboxstrm',
    5417089:'ITmailinboxstrm',
    5417094:'FRmailinboxstrm',
    5417109:'beautymagazinestrm',
    5417150:'ARanswersstrm',
    5417151:'AUmailleftrailstrm',
    5417165:'BRanswersstrm',
    5417170:'CAanswersstrm',
    5417186:'ESanswersstrm',
    5417208:'ITanswersstrm',
    5417213:'MXanswersstrm',
    5417255:'USanswersstrm-es',
    5417337:'XE_XAhomepagestrm-ar',
    5417383:'gmastrm',
    5417407:'gmacontentstrm',
    5417810:'newssidekickarticlestrm',
    5417814:'sportssidekickarticlestrm',
    5417818:'financesidekickarticlestrm',
    5417826:'celebritysidekickarticlestrm',
    5417830:'tvsidekickarticlestrm',
    5417946:'attsbcportalstrm-US-es',
    5417978:'Ad Unit 9/2/2014 7:05:56 PM',
    5417979:'mailnewsstrm',
    5418078:'att_search_mobile_yhs_curve_mobile',
    5418137:'yhs-mobotap_dolphin_mobile_search_curve_mobile',
    5418222:'att_yhs06_search_curve_tablet',
    5418421:'TWautosstrm',
    5418519:'sandvine_error_mobile_curve_mobile',
    5418521:'litmus_mobile-default_curve_mobile',
    5418523:'adknowledge_mobile_1click_search_curve_mobile',
    5418527:'timewarner_rr_error_twc_mobile_curve_mobile',
    5418528:'bmv_classifiedads_mobile2_search_curve_mobile',
    5418549:'geosign_oo_mobi_1_search_curve_mobile',
    5418561:'bmv_classifiedads_mobile2_search_curve_tablet',
    5418570:'geosign_oo_mobi_2_search_curve_mobile',
    5418571:'geosign_oo_mobi_3_search_curve_mobile',
    5418599:'geosign_mobilemom_mobile_search_curve_mobile',
    5418600:'geosign_mobile_facebooktwo_curve_mobile',
    5418619:'distinct_xml_us_searchbox_googlec3_curve_mobile',
    5418629:'distinct_xml_us_searchbox_local_curve_mobile',
    5418636:'distinct_xml_us_searchbox_googlec3_curve_tablet',
    5418671:'distinct_xml_us_searchbox_msnsearch_curve_mobile',
    5418672:'intercosmos_crow_search_curve_mobile',
    5418673:'ibario_xml_search_curve_tablet',
    5418679:'bmv_classifiedads_msr_search_curve_mobile',
    5418694:'intercosmos_crow_search_curve_tablet',
    5418708:'distinct_xml_us_searchbox_googlesearch_curve_tablet',
    5418754:'intercosmos_chopstick_search_curve_mobile',
    5418756:'distinct_xml_us_searchbox_googlesearch_curve_mobile',
    5418767:'intercosmos_chopstick_search_curve_tablet',
    5418873:'intercosmos_dugout_search_curve_mobile',
    5418881:'intercosmos_dugout_search_curve_tablet',
    5418972:'distinct_xml_us_searchbox_googlesearch3_curve_mobile',
    5419034:'ibario_xml_search_curve_mobile',
    5419095:'distinct_xml_us_searchbox_googlesearch17_curve_mobile',
    5419359:'geosign_oo_84_search_curve_mobile',
    5419497:'litmus_search-oando6_curve_tablet',
    5419522:'litmus_search-oando10_curve_tablet',
    5419523:'distinct_xml_us_searchbox_facebook1_curve_mobile',
    5419580:'litmus_search-oando6_curve_mobile',
    5419759:'adconion_us_search_curve_mobile',
    5419761:'adknowledge_2click_search_b_curve_mobile',
    5419954:'TWsidekickclassicnews',
    5419956:'SidekickClassicBRNews',
    5419959:'SidekickClassicCANews',
    5419960:'SidekickClassicSGNews',
    5419985:'hpsidekickmobilestrm',
    5420096:'financenative_android_strm',
    5420216:'SidekickClassicCAFinance',
    5420222:'SidekickClassicDENews',
    5420226:'SidekickClassicESNews',
    5420229:'SidekickClassicFRNews',
    5420230:'SidekickClassicGBFinance',
    5420231:'SidekickClassicGBNews',
    5420234:'SidekickClassicHKFinance',
    5420236:'SidekickClassicHKNews',
    5420237:'SidekickClassicHKCelebrity',
    5420244:'SidekickClassicINNews',
    5420261:'SidekickClassicTWCelebrity',
    5420263:'SidekickClassicEsUSNews',
    5420334:'ETtoday_mobile_one_ads_po2',
    5420448:'yahoo_local_bpp_ros_derp_curve_tablet',
    5420624:'SidekickClassicITNews'
};

var section_whitelist = {
    4421334:'newsministrm',
    4402687:'newsmainstrm',
    4492584:'sportsministrm',
    4492794:'financeministrm',
    4250754:'hpstrm',
    5354120:'tumblrmobilestrm',
    5496342:'tumblrBlogInstream',
    4923847:'postcardinboxstrm',
    5421583:'mailmsgliststrm-Norrin',
    4871337:'mailandroidappstrm',
    5317864:'mailiosappstrm',
    5324856:'mailnativemobile',
    5192354:'tumblrstrm',
    5420470:'Tango-Carousel',
    5420469:'Tango-Chat',
    4494903:'hmrnstrm',
    5413706:'fantasyiosappstrm',
    5413723:'homerununifiedappandroidstrm',
    5413718:'hmrnandroidstrm',
    5413705:'fantasyandroidappstrm',
    5447576:'Tango-profile-ios',
    5447578:'Tango-feed-ios',
    5447579:'Tango-chat-ios',
    5447580:'Tango-discover-ios',
    5447581:'Tango-profile-android',
    5447582:'Tango-feed-android',
    5447583:'Tango-chat-android',
    5447584:'Tango-discover-android',
    5459020:'Cheetah-Applock-BigNative',
    5463970:'Cheetah-ChargingScreen-BigNative',
    5463955:'SDK-Cheetah-Applock-BigNative',
    5463954:'SDK-Cheetah-ChargingScreen-BigNative'
};



function get_param(tabid) {
    if(tabid == 'topsection') {
        return {'section': Object.keys(topsections).join(',')};
    } else if (tabid == 'section_whitelist') {
        return {'section': Object.keys(section_whitelist).join(',')};
    }
    return null;
}

function ranking_keys(maps) {
    var array = [];
    Object.keys(maps).forEach(function(key) {
        var sum = 0;
        maps[key].forEach(function(item){
            sum += item[1];
        });
        array.push([key, sum]);
    });
    array.sort(function(a, b) {
        return b[1] - a[1];
    });
    return array.map(function(item) {
        return item[0];
    }).slice(0,30);
}

function convert_title(section_id) {
    var sectionName = (section_id in topsections) ? 
            topsections[section_id] : section_whitelist[section_id];
    return "{0}({1})".format(sectionName, section_id)
}

function show(chart, result) {

    load_script("js/triage.js", function() {
        show(chart, result, ranking_keys, convert_title);
    });

}
