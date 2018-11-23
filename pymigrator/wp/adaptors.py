from ..core.adaptors import BaseAdaptor


class PostsAdaptor(BaseAdaptor):
    @property
    def id(self):
        return self.dict_obj['ID']

    @id.setter
    def id(self, value):
        self.dict_obj['ID'] = value

    @property
    def post_author(self):
        return self.dict_obj['post_author']

    @post_author.setter
    def post_author(self, value):
        self.dict_obj['post_author'] = value

    @property
    def post_date(self):
        return self.dict_obj['post_date']

    @post_date.setter
    def post_date(self, value):
        self.dict_obj['post_date'] = value

    @property
    def post_date_gmt(self):
        return self.dict_obj['post_date_gmt']

    @post_date_gmt.setter
    def post_date_gmt(self, value):
        self.dict_obj['post_date_gmt'] = value

    @property
    def post_content(self):
        return self.dict_obj['post_content']

    @post_content.setter
    def post_content(self, value):
        self.dict_obj['post_content'] = value

    @property
    def post_title(self):
        return self.dict_obj['post_title']

    @post_title.setter
    def post_title(self, value):
        self.dict_obj['post_title'] = value

    @property
    def post_excerpt(self):
        return self.dict_obj['post_excerpt']

    @post_excerpt.setter
    def post_excerpt(self, value):
        self.dict_obj['post_excerpt'] = value

    @property
    def post_status(self):
        return self.dict_obj['post_status']

    @post_status.setter
    def post_status(self, value):
        self.dict_obj['post_status'] = value

    @property
    def comment_status(self):
        return self.dict_obj['comment_status']

    @comment_status.setter
    def comment_status(self, value):
        self.dict_obj['comment_status'] = value

    @property
    def ping_status(self):
        return self.dict_obj['ping_status']

    @ping_status.setter
    def ping_status(self, value):
        self.dict_obj['ping_status'] = value

    @property
    def post_password(self):
        return self.dict_obj['post_password']

    @post_password.setter
    def post_password(self, value):
        self.dict_obj['post_password'] = value

    @property
    def post_name(self):
        return self.dict_obj['post_name']

    @post_name.setter
    def post_name(self, value):
        self.dict_obj['post_name'] = value

    @property
    def to_ping(self):
        return self.dict_obj['to_ping']

    @to_ping.setter
    def to_ping(self, value):
        self.dict_obj['to_ping'] = value

    @property
    def pinged(self):
        return self.dict_obj['pinged']

    @pinged.setter
    def pinged(self, value):
        self.dict_obj['pinged'] = value

    @property
    def post_modified(self):
        return self.dict_obj['post_modified']

    @post_modified.setter
    def post_modified(self, value):
        self.dict_obj['post_modified'] = value

    @property
    def post_modified_gmt(self):
        return self.dict_obj['post_modified_gmt']

    @post_modified_gmt.setter
    def post_modified_gmt(self, value):
        self.dict_obj['post_modified_gmt'] = value

    @property
    def post_content_filtered(self):
        return self.dict_obj['post_content_filtered']

    @post_content_filtered.setter
    def post_content_filtered(self, value):
        self.dict_obj['post_content_filtered'] = value

    @property
    def post_parent(self):
        return self.dict_obj['post_parent']

    @post_parent.setter
    def post_parent(self, value):
        self.dict_obj['post_parent'] = value

    @property
    def guid(self):
        return self.dict_obj['guid']

    @guid.setter
    def guid(self, value):
        self.dict_obj['guid'] = value

    @property
    def menu_order(self):
        return self.dict_obj['menu_order']

    @menu_order.setter
    def menu_order(self, value):
        self.dict_obj['menu_order'] = value

    @property
    def post_type(self):
        return self.dict_obj['post_type']

    @post_type.setter
    def post_type(self, value):
        self.dict_obj['post_type'] = value

    @property
    def post_mime_type(self):
        return self.dict_obj['post_mime_type']

    @post_mime_type.setter
    def post_mime_type(self, value):
        self.dict_obj['post_mime_type'] = value

    @property
    def comment_count(self):
        return self.dict_obj['comment_count']

    @comment_count.setter
    def comment_count(self, value):
        self.dict_obj['comment_count'] = value

    @classmethod
    def get_header(cls):
        return [
            'ID',
            'post_author',
            'post_date',
            'post_date_gmt',
            'post_content',
            'post_title',
            'post_excerpt',
            'post_status',
            'comment_status',
            'ping_status',
            'post_password',
            'post_name',
            'to_ping',
            'pinged',
            'post_modified',
            'post_modified_gmt',
            'post_content_filtered',
            'post_parent',
            'guid',
            'menu_order',
            'post_type',
            'post_mime_type',
            'comment_count',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'ID'

    @classmethod
    def get_default_values(cls):
        return zip(
            cls.get_header(),
            [
                '',  # ID
                '0',  # post_author
                '0000-00-00 00:00:00',  # post_date
                '0000-00-00 00:00:00',  # post_date_gmt
                '',  # post_content
                '',  # post_title
                '',  # post_excerpt
                'publish',  # post_status
                'open',  # comment_status
                'open',  # ping_status
                '',  # post_password
                '',  # post_name
                '',  # to_ping
                '',  # pinged
                '0000-00-00 00:00:00',  # post_modified
                '0000-00-00 00:00:00',  # post_modified_gmt
                '',  # post_content_filtered
                '0',  # post_parent
                '',  # guid
                '0',  # menu_order
                'post',  # post_type
                '',  # post_mime_type
                '0',  # comment_count
            ]
        )


class PostMetaAdaptor(BaseAdaptor):
    @property
    def meta_id(self):
        return self.dict_obj['meta_id']

    @meta_id.setter
    def meta_id(self, value):
        self.dict_obj['meta_id'] = value

    @property
    def post_id(self):
        return self.dict_obj['post_id']

    @post_id.setter
    def post_id(self, value):
        self.dict_obj['post_id'] = value

    @property
    def meta_key(self):
        return self.dict_obj['meta_key']

    @meta_key.setter
    def meta_key(self, value):
        self.dict_obj['meta_key'] = value

    @property
    def meta_value(self):
        return self.dict_obj['meta_value']

    @meta_value.setter
    def meta_value(self, value):
        self.dict_obj['meta_value'] = value

    @classmethod
    def get_header(cls):
        return [
            'meta_id',
            'post_id',
            'meta_key',
            'meta_value',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'meta_id'


class UserAdaptor(BaseAdaptor):
    @property
    def id(self):
        return self.dict_obj['ID']

    @id.setter
    def id(self, value):
        self.dict_obj['ID'] = value

    @property
    def user_login(self):
        return self.dict_obj['user_login']

    @user_login.setter
    def user_login(self, value):
        self.dict_obj['user_login'] = value

    @property
    def user_pass(self):
        return self.dict_obj['user_pass']

    @user_pass.setter
    def user_pass(self, value):
        self.dict_obj['user_pass'] = value

    @property
    def user_nicename(self):
        return self.dict_obj['user_nicename']

    @user_nicename.setter
    def user_nicename(self, value):
        self.dict_obj['user_nicename'] = value

    @property
    def user_email(self):
        return self.dict_obj['user_email']

    @user_email.setter
    def user_email(self, value):
        self.dict_obj['user_email'] = value

    @property
    def user_url(self):
        return self.dict_obj['user_url']

    @user_url.setter
    def user_url(self, value):
        self.dict_obj['user_url'] = value

    @property
    def user_registered(self):
        return self.dict_obj['user_registered']

    @user_registered.setter
    def user_registered(self, value):
        self.dict_obj['user_registered'] = value

    @property
    def user_activation_key(self):
        return self.dict_obj['user_activation_key']

    @user_activation_key.setter
    def user_activation_key(self, value):
        self.dict_obj['user_activation_key'] = value

    @property
    def user_status(self):
        return self.dict_obj['user_status']

    @user_status.setter
    def user_status(self, value):
        self.dict_obj['user_status'] = value

    @property
    def display_name(self):
        return self.dict_obj['display_name']

    @display_name.setter
    def display_name(self, value):
        self.dict_obj['display_name'] = value

    @classmethod
    def get_header(cls):
        return [
            'ID',
            'user_login',
            'user_pass',
            'user_nicename',
            'user_email',
            'user_url',
            'user_registered',
            'user_activation_key',
            'user_status',
            'display_name',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'ID'

    @classmethod
    def get_default_values(cls):
        return zip(
            cls.get_header(),
            [
                '',  # ID
                '',  # user_login
                '',  # user_pass
                '',  # user_nicename
                '',  # user_email
                '',  # user_url
                '0000-00-00 00:00:00',  # user_registered
                '',  # user_activation_key
                '0',  # user_status
                '',  # display_name
            ]
        )


class MultiSiteUserAdaptor(UserAdaptor):
    @property
    def spam(self):
        return self.dict_obj['spam']

    @spam.setter
    def spam(self, value):
        self.dict_obj['spam'] = value

    @property
    def deleted(self):
        return self.dict_obj['deleted']

    @deleted.setter
    def deleted(self, value):
        self.dict_obj['deleted'] = value

    @classmethod
    def get_header(cls):
        return UserAdaptor.get_header() + ['spam', 'deleted']

    @classmethod
    def get_default_values(cls):
        return zip(
            cls.get_header(),
            [
                '',  # ID
                '',  # user_login
                '',  # user_pass
                '',  # user_nicename
                '',  # user_email
                '',  # user_url
                '0000-00-00 00:00:00',  # user_registered
                '',  # user_activation_key
                '0',  # user_status
                '',  # display_name
                '0',  # spam
                '0',  # deleted
            ]
        )


class UserMetaAdaptor(BaseAdaptor):
    @property
    def umeta_id(self):
        return self.dict_obj['umeta_id']

    @umeta_id.setter
    def umeta_id(self, value):
        self.dict_obj['umeta_id'] = value

    @property
    def user_id(self):
        return self.dict_obj['user_id']

    @user_id.setter
    def user_id(self, value):
        self.dict_obj['user_id'] = value

    @property
    def meta_key(self):
        return self.dict_obj['meta_key']

    @meta_key.setter
    def meta_key(self, value):
        self.dict_obj['meta_key'] = value

    @property
    def meta_value(self):
        return self.dict_obj['meta_value']

    @meta_value.setter
    def meta_value(self, value):
        self.dict_obj['meta_value'] = value

    @classmethod
    def get_header(cls):
        return [
            'umeta_id',
            'user_id',
            'meta_key',
            'meta_value',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'umeta_id'


class OptionsAdaptor(BaseAdaptor):
    @property
    def option_id(self):
        return self.dict_obj['option_id']

    @option_id.setter
    def option_id(self, value):
        self.dict_obj['option_id'] = value

    @property
    def option_name(self):
        return self.dict_obj['option_name']

    @option_name.setter
    def option_name(self, value):
        self.dict_obj['option_name'] = value

    @property
    def option_value(self):
        return self.dict_obj['option_value']

    @option_value.setter
    def option_value(self, value):
        self.dict_obj['option_value'] = value

    @property
    def autoload(self):
        return self.dict_obj['autoload']

    @autoload.setter
    def autoload(self, value):
        self.dict_obj['autoload'] = value

    @classmethod
    def get_header(cls):
        return [
            'option_id',
            'option_name',
            'option_value',
            'autoload',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'option_id'


class TermsAdaptor(BaseAdaptor):
    @property
    def term_id(self):
        return self.dict_obj['term_id']

    @term_id.setter
    def term_id(self, value):
        self.dict_obj['term_id'] = value

    @property
    def name(self):
        return self.dict_obj['name']

    @name.setter
    def name(self, value):
        self.dict_obj['name'] = value

    @property
    def slug(self):
        return self.dict_obj['slug']

    @slug.setter
    def slug(self, value):
        self.dict_obj['slug'] = value

    @property
    def term_group(self):
        return self.dict_obj['term_group']

    @term_group.setter
    def term_group(self, value):
        self.dict_obj['term_group'] = value

    @classmethod
    def get_header(cls):
        return [
            'term_id',
            'name',
            'slug',
            'term_group',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'term_id'


class TermMetaAdaptor(BaseAdaptor):
    @property
    def meta_id(self):
        return self.dict_obj['meta_id']

    @meta_id.setter
    def meta_id(self, value):
        self.dict_obj['meta_id'] = value

    @property
    def term_id(self):
        return self.dict_obj['term_id']

    @term_id.setter
    def term_id(self, value):
        self.dict_obj['term_id'] = value

    @property
    def meta_key(self):
        return self.dict_obj['meta_key']

    @meta_key.setter
    def meta_key(self, value):
        self.dict_obj['meta_key'] = value

    @property
    def meta_value(self):
        return self.dict_obj['meta_value']

    @meta_value.setter
    def meta_value(self, value):
        self.dict_obj['meta_value'] = value

    @classmethod
    def get_header(cls):
        return [
            'meta_id',
            'term_id',
            'meta_key',
            'meta_value',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'meta_id'


class TermTaxonomyAdaptor(BaseAdaptor):
    @property
    def term_taxonomy_id(self):
        return self.dict_obj['term_taxonomy_id']

    @term_taxonomy_id.setter
    def term_taxonomy_id(self, value):
        self.dict_obj['term_taxonomy_id'] = value

    @property
    def term_id(self):
        return self.dict_obj['term_id']

    @term_id.setter
    def term_id(self, value):
        self.dict_obj['term_id'] = value

    @property
    def taxonomy(self):
        return self.dict_obj['taxonomy']

    @taxonomy.setter
    def taxonomy(self, value):
        self.dict_obj['taxonomy'] = value

    @property
    def description(self):
        return self.dict_obj['description']

    @description.setter
    def description(self, value):
        self.dict_obj['description'] = value

    @property
    def parent(self):
        return self.dict_obj['parent']

    @parent.setter
    def parent(self, value):
        self.dict_obj['parent'] = value

    @property
    def count(self):
        return self.dict_obj['count']

    @count.setter
    def count(self, value):
        self.dict_obj['count'] = value

    @classmethod
    def get_header(cls):
        return [
            'term_taxonomy_id',
            'term_id',
            'taxonomy',
            'description',
            'parent',
            'count',
        ]

    @classmethod
    def get_ai_field(cls):
        return 'term_taxonomy_id'


class TermRelationShipsAdaptor(BaseAdaptor):
    @property
    def object_id(self):
        return self.dict_obj['object_id']

    @object_id.setter
    def object_id(self, value):
        self.dict_obj['object_id'] = value

    @property
    def term_taxonomy_id(self):
        return self.dict_obj['term_taxonomy_id']

    @term_taxonomy_id.setter
    def term_taxonomy_id(self, value):
        self.dict_obj['term_taxonomy_id'] = value

    @property
    def term_order(self):
        return self.dict_obj['term_order']

    @term_order.setter
    def term_order(self, value):
        self.dict_obj['term_order'] = value

    @classmethod
    def get_header(cls):
        return [
            'object_id',
            'term_taxonomy_id',
            'term_order',
        ]
