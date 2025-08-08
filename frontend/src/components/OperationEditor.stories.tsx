import React from 'react';
import { ComponentStory, ComponentMeta } from '@storybook/react';
import OperationEditor from './OperationEditor';

export default {
  title: 'Components/OperationEditor',
  component: OperationEditor
} as ComponentMeta<typeof OperationEditor>;

const Template: ComponentStory<typeof OperationEditor> = (args) => <OperationEditor {...args} />;

export const Default = Template.bind({});
Default.args = {};
