define(["views/view_article/article","views/common/article_edit_modal"],function(e,t){var n=e.extend({className:"article pending",events:_.extend(e.prototype.events,{"click .js-edit":"onClickEdit","click .js-reject":"onClickReject","click .js-approve":"onClickApprove"}),onRender:function(){e.prototype.onRender.apply(this,arguments),this.ui.sidebar.append($("#sidebar-action-template").html())},onClickEdit:function(e){this.modal=new t({model:this.model}),this.modal.render()},onClickReject:function(e){var t=this;this.model.destroy({wait:!0}).complete(function(){}).success(function(){})},onClickApprove:function(e){var t=this;this.model.approve().complete(function(){}).success(function(){t.model.collection.remove(t.model)})}});return n});