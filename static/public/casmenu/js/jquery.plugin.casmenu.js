(function($){
	//配置
	var AI={
		opts:{
			saveinput:"jumpcode", //是否将结果保存至input
			levels:{},
			ulObj:{},//保存生成好的ul列表
			length:0, //层级菜单的层级
			divide:",",//默认各个层级菜单之间的分隔符
		}
	};

	$.fn.casmenu=function(opts){
		AI.opts = $.extend(AI.opts, opts);

		if((AI.opts.length = Object.keys(AI.opts.levels).length) <= 0){
			throw "levels arr must not be empty";
			return;
		}

		var _levels = AI.opts.levels;
		if(_levels[1] == undefined){
			throw "menu level 1 must not be empty";
			return;
		}
		var _levels_1 = _levels[1];

		if(typeof(AI.opts.saveinput) != "undefined" && (AI.opts.saveinput = AI.opts.saveinput.toString()) != ''){
			$("<input type='hidden' value='' name='"+AI.opts.saveinput+"' id='"+AI.opts.saveinput+"' />").appendTo($('body'));
		}

		AI.opts.ulObj['level_1'] = '<select class="casmenu" level="1">';
		AI.opts.ulObj['level_1'] += '<option value="null">请选择</option>';
		$("#"+AI.opts.saveinput).val('null');
		for(var i in _levels_1){
			AI.opts.ulObj['level_1'] += '<option name="'+i+'" value="'+_levels_1[i]+'">'+i+'</option>';
		}
		AI.opts.ulObj['level_1'] += '</select>';

		$(AI.opts.ulObj['level_1']).appendTo(this);

		$("body").on("change", ".casmenu", function(){
			var level = $(this).attr("level");
			if(level > AI.opts.length) return;
			level++;
			//移除当前触发菜单之后的菜单
			for(var num=level;num<=AI.opts.length;num++){
				$(".casmenu[level="+num+"]").remove();
			}

			//设置input的值，级联菜单的值
			var _val = '';
			for(var val=1;val<=AI.opts.length;val++){
				var __val = $("select[level="+val+"]");
				if(__val.length <= 0)
					continue;

				_val += __val.val()+AI.opts.divide;
			}
			$("#"+AI.opts.saveinput).val(_val.substr(0, _val.length-1));

			//levels对象中不存在下一级别目录
			if(typeof(AI.opts.levels[level]) == "undefined") return;

			//获取下一级别目录的键值，值不存在的话返回
			var name = $(this).find("option:selected").attr("name");
			if(typeof(AI.opts.levels[level][name]) == "undefined") return;

			if(typeof(AI.opts.ulObj['level_'+level]) == "undefined" || typeof(AI.opts.ulObj['level_'+level][name]) == "undefined"){
				if(typeof(AI.opts.ulObj['level_'+level]) == "undefined")
					AI.opts.ulObj['level_'+level] = {};

				AI.opts.ulObj['level_'+level][name] = '<select class="casmenu" level="'+level+'">';
				AI.opts.ulObj['level_'+level][name] += '<option value="null">请选择</option>';
				var levelinfo = AI.opts.levels[level][name];
				for(var i in levelinfo){
					AI.opts.ulObj['level_'+level][name] += '<option name="'+i+'" value="'+levelinfo[i]+'" >'+i+'</option>';
				}
				AI.opts.ulObj['level_'+level][name] += '</select>';
			}
			$(AI.opts.ulObj['level_'+level][name]).appendTo($(this).parent());
			var _val = '';
			for(var val=1;val<=AI.opts.length;val++){
				var __val = $("select[level="+val+"]");
				if(__val.length <= 0)
					continue;

				_val += __val.val()+AI.opts.divide;
			}
			$("#"+AI.opts.saveinput).val(_val.substr(0, _val.length-1));
		});
	}
})(jQuery);