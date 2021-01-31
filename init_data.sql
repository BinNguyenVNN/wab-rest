INSERT INTO public.notify_channel(id, name, type, description, template, config, active) VALUES
(1, 'email', 'email', 'email', 'email', null, true),
(2, 'push_notification', 'push_notification', 'push_notification', 'push_notification', null, true);

ALTER SEQUENCE public.notify_channel_id_seq RESTART WITH 2;
