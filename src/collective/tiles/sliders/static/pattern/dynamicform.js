/* global define */

define([
  'jquery',
  'mockup-patterns-base',
  'mockup-utils'
], function($, Base, utils) {
  'use strict';

  var FormPattern = Base.extend({
    name: 'dynamicform',
    trigger: '.pat-dynamicform',
    parser: 'mockup',
    defaults: {
    },
    init: function() {
      var self = this;
      var $form = self.$el.parents('form');
      if($form.size() === 0){
        return;
      }
      self.$form = $form;
      self.bind();
      self.manipulate();
    },
    manipulate: function(){
      // show/hide stuff
      var self = this;
      var $useQuery = self.getUseQuery();
      if($useQuery.size() === 1){
        if($('input', self.getUseQuery())[0].checked){
          self.getQuery().show();
          self.getLimit().show();
          self.getContent().hide();
        }else{
          self.getQuery().hide();
          self.getLimit().hide();
          self.getContent().show();
        }
      }
    },
    bind: function(){
      var self = this;
      $('input', self.getUseQuery()).change(function(){
        self.manipulate();
      });
    },
    getLimit: function(){
      return $('div[id$="-limit"]', this.$form);
    },
    getUseQuery: function(){
      return $('div[id$="-use_query"]', this.$form);
    },
    getQuery: function(){
      return $('div[id$="-query"]', this.$form);
    },
    getContent: function(){
      return $('div[id$="-content"],div[id$="-images"]', this.$form);
    },
  });
  return FormPattern;

});
